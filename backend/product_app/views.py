from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Product
from .serializers import ProductSerializer
from .pagination import ProductPagination

class ProductListCreateView(APIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = ProductPagination

    def get(self, request):
        products = Product.objects.all()
        paginator = ProductPagination()
        results = paginator.paginate_queryset(products, request)
        serializer = ProductSerializer(results, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductDetailView(APIView):
    def get(self, request, product_id):
        try:
            product = get_object_or_404(Product, id=product_id)
            serializer = ProductSerializer(product)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "Product retrieval failed", "details": str(e)}, status=status.HTTP_400_BAD_REQUEST)


    def put(self, request, product_id):
        try:
            product = get_object_or_404(Product, id=product_id)
            serializer = ProductSerializer(product, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({"error": "Validation failed", "details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": "Product update failed", "details": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, product_id):
        try:
            product = get_object_or_404(Product, id=product_id)
            product.delete()
            return Response({"message": "Product deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": "Product deletion failed", "details": str(e)}, status=status.HTTP_400_BAD_REQUEST)
