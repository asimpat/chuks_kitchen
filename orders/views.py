from rest_framework.views import APIView
from rest_framework.response import Response
from auths.permissions import IsCustomer, IsAdmin
from .serializers import PlaceOrderSerializer, OrderSerializer, UpdateOrderStatusSerializer
from .models import Order


class PlaceOrderView(APIView):
    permission_classes = [IsCustomer]

    def post(self, request):
        serializer = PlaceOrderSerializer(
            data=request.data,
            context={'request': request}
        )
        
        if serializer.is_valid():
            order = serializer.save()
            return Response({
                "success": True,
                "message": "Order placed successfully! We'll confirm shortly.",
                "order_id": order.id,
                "total_price": str(order.total_price),
                "status": order.status,
                "payment_status": order.payment_status
            }, status=201)

        return Response({"success": False, "errors": serializer.errors}, status=400)


class CustomerOrderListView(APIView):
    permission_classes = [IsCustomer]

    def get(self, request):
        orders = Order.objects.filter(
            customer=request.user
        ).prefetch_related('items__food_item').order_by('-created_at')

        serializer = OrderSerializer(orders, many=True)
        return Response({"success": True, "data": serializer.data})


class CustomerOrderDetailView(APIView):
    permission_classes = [IsCustomer]

    def get(self, request, pk):
        try:
            order = Order.objects.prefetch_related('items__food_item').get(
                pk=pk,
                customer=request.user
            )
        except Order.DoesNotExist:
            return Response({"success": False, "message": "Order not found"}, status=404)

        serializer = OrderSerializer(order)
        return Response({"success": True, "data": serializer.data})


class CustomerCancelOrderView(APIView):
    permission_classes = [IsCustomer]

    def patch(self, request, pk):
        try:
            order = Order.objects.get(pk=pk, customer=request.user)
        except Order.DoesNotExist:
            return Response({"success": False, "message": "Order not found"}, status=404)

        if order.status != 'pending':
            return Response({
                "success": False,
                "message": f"Cannot cancel order. Current status is '{order.status}'. Only pending orders can be cancelled."
            }, status=400)

        order.status = 'cancelled'
        order.save()
        return Response({"success": True, "message": "Your order has been cancelled."})


class AdminOrderListView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        status_filter = request.query_params.get('status')
        orders = Order.objects.prefetch_related(
            'items__food_item').order_by('-created_at')

        if status_filter:
            orders = orders.filter(status=status_filter)

        serializer = OrderSerializer(orders, many=True)
        return Response({"success": True, "count": orders.count(), "data": serializer.data})


class AdminUpdateOrderStatusView(APIView):
    permission_classes = [IsAdmin]

    def patch(self, request, pk):
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response({"success": False, "message": "Order not found"}, status=404)

        serializer = UpdateOrderStatusSerializer(data=request.data)
        if serializer.is_valid():
            new_status = serializer.validated_data['status']

            # Prevent updating a completed or cancelled order
            if order.status in ['completed', 'cancelled']:
                return Response({
                    "success": False,
                    "message": f"Cannot update a {order.status} order."
                }, status=400)

            order.status = new_status
            order.save()
            return Response({
                "success": True,
                "message": f"Order #{pk} status updated to '{new_status}'"
            })

        return Response({"success": False, "errors": serializer.errors}, status=400)
