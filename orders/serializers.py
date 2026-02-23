from rest_framework import serializers
from .models import Order, OrderItem
from foods.models import FoodItem


class OrderItemInputSerializer(serializers.Serializer):
    food_item_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)


class PlaceOrderSerializer(serializers.Serializer):
    items = OrderItemInputSerializer(many=True)
    delivery_address = serializers.CharField(required=False, allow_blank=True)
    note = serializers.CharField(required=False, allow_blank=True)

    def validate_items(self, items):
        if not items:
            raise serializers.ValidationError(
                "You must include at least one item")
        return items

    def create(self, validated_data):
        customer = self.context['request'].user
        items_data = validated_data['items']
        total = 0
        order_items_to_create = []

        # Step 1: Validate ALL items before creating anything
        # We don't want to create a half-order if one item fails
        for item_data in items_data:
            try:
                food = FoodItem.objects.get(pk=item_data['food_item_id'])
            except FoodItem.DoesNotExist:
                raise serializers.ValidationError(
                    f"Food item with ID {item_data['food_item_id']} does not exist"
                )

            if not food.is_available:
                raise serializers.ValidationError(
                    f"'{food.name}' is currently unavailable. Please remove it from your order."
                )

            subtotal = food.price * item_data['quantity']
            total += subtotal
            order_items_to_create.append({
                'food': food,
                'quantity': item_data['quantity'],
                'unit_price': food.price  # snapshot the current price
            })

        # Step 2: Create the order
        order = Order.objects.create(
            customer=customer,
            total_price=total,
            delivery_address=validated_data.get('delivery_address', ''),
            note=validated_data.get('note', '')
        )

        # Step 3: Create each order item
        for item in order_items_to_create:
            OrderItem.objects.create(
                order=order,
                food_item=item['food'],
                quantity=item['quantity'],
                unit_price=item['unit_price']
            )

        return order


class OrderItemSerializer(serializers.ModelSerializer):
    """Used when showing order details"""
    food_name = serializers.CharField(source='food_item.name', read_only=True)
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ['food_name', 'quantity', 'unit_price', 'subtotal']

    def get_subtotal(self, obj):
        return obj.get_subtotal()


class OrderSerializer(serializers.ModelSerializer):
    """Full order with all its items — used in list and detail views"""
    items = OrderItemSerializer(many=True, read_only=True)
    customer_email = serializers.CharField(
        source='customer.email', read_only=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'customer_email',
            'status',
            'total_price',
            'delivery_address',
            'note',
            'items',
            'created_at',
            'updated_at'
        ]


class UpdateOrderStatusSerializer(serializers.Serializer):
    """Admin uses this to update order status"""
    status = serializers.ChoiceField(choices=Order.STATUS_CHOICES)
