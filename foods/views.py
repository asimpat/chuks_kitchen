from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import FoodItem, Category
from .serializers import FoodItemSerializer, CategorySerializer
from auths.permissions import IsAdmin


class CategoryListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response({"success": True, "data": serializer.data})


class AdminCategoryView(APIView):
    permission_classes = [IsAdmin]

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "data": serializer.data}, status=201)
        return Response({"success": False, "errors": serializer.errors}, status=400)
    
    def patch(self, request, pk):
        try:
            item = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response({"success": False, "message": "Category not found"}, status=404)

        serializer = CategorySerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "data": serializer.data})
        return Response({"success": False, "errors": serializer.errors}, status=400)


class FoodItemListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        items = FoodItem.objects.filter(is_available=True)
        serializer = FoodItemSerializer(items, many=True)
        return Response({"success": True, "data": serializer.data})


class AdminFoodItemView(APIView):
    permission_classes = [IsAdmin]

    def post(self, request):
        serializer = FoodItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "data": serializer.data}, status=201)
        return Response({"success": False, "errors": serializer.errors}, status=400)

    def patch(self, request, pk):
        try:
            item = FoodItem.objects.get(pk=pk)
        except FoodItem.DoesNotExist:
            return Response({"success": False, "message": "Item not found"}, status=404)

        serializer = FoodItemSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "data": serializer.data})
        return Response({"success": False, "errors": serializer.errors}, status=400)

