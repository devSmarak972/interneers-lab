from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ProductSerializer, ProductCategorySerializer, ProductFilterSerializer
from .pagination import ProductPagination
from .services import ProductService, ProductCategoryService, ProductService
from rest_framework.generics import ListAPIView

class ProductListCreateView(ListAPIView):
    serializer_class = ProductSerializer
    pagination_class = ProductPagination

    def get_queryset(self):
        return ProductService.list_products()

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            try:
                product = ProductService.create_product(serializer.validated_data)
                return Response(ProductSerializer(product).data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": "Failed to create product", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({"error": "Validation failed", "details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class ProductDetailView(APIView):
    serializer_class = ProductSerializer

    def get(self, request, product_id):
        product = ProductService.get_product(product_id)
        if product:
            return Response(ProductSerializer(product).data, status=status.HTTP_200_OK)
        return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, product_id):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            try:
                product = ProductService.update_product(product_id, serializer.validated_data)
                if product:
                    return Response(ProductSerializer(product).data, status=status.HTTP_200_OK)
                return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({"error": "Failed to update product", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({"error": "Validation failed", "details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, product_id):
        try:
            if ProductService.delete_product(product_id):
                return Response({"message": "Product deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": "Failed to delete product", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class ProductCategoryListCreateView(APIView):
    """
    API View for listing and creating product categories.
    """
    serializer_class = ProductCategorySerializer

    def get(self, request):
        categories = ProductCategoryService.list_categories()
        return Response(ProductCategorySerializer(categories, many=True).data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ProductCategorySerializer(data=request.data)
        if serializer.is_valid():
            try:
                category = ProductCategoryService.create_category(serializer.validated_data)
                return Response(ProductCategorySerializer(category).data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": "Failed to create category", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({"error": "Validation failed", "details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            
class ProductByCategoryView(APIView):
    """
    API View to fetch products by category.
    """
    serializer_class = ProductCategorySerializer

    def get(self, request, category_id):
        products = ProductService.get_products_by_category(category_id)
        return Response(ProductSerializer(products, many=True).data, status=status.HTTP_200_OK)
    
    def post(self, request):
        """
        Create or update a product category.
        """
        serializer = ProductCategorySerializer(data=request.data)

        if serializer.is_valid():
            category = ProductCategoryService.create_or_update_category(serializer.validated_data)
            if category:
                return Response(ProductCategorySerializer(category).data, status=status.HTTP_200_OK)
            return Response({"error": "Category not found."}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, category_id):
        """
        Delete a category and update associated products to 'Uncategorized'.
        """
        success = ProductCategoryService.delete_category(category_id)

        if success:
            return Response({"message": "Category deleted, products reassigned."}, status=status.HTTP_200_OK)
        return Response({"error": "Category not found."}, status=status.HTTP_404_NOT_FOUND)

class ProductManageByCategoryView(APIView):
    """
    API View to fetch products by category.
    """

    def post(self, request, category_id, product_id):
        product = ProductService.add_product_to_category(product_id, category_id)
        if product:
            return Response(ProductSerializer(product).data, status=status.HTTP_200_OK)
        return Response({"error": "Invalid product or category"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, product_id):
        product = ProductService.remove_product_from_category(product_id)
        if product:
            return Response(ProductSerializer(product).data, status=status.HTTP_200_OK)
        return Response({"error": "Product not found"}, status=status.HTTP_400_BAD_REQUEST)


from rest_framework.decorators import api_view

@api_view(['GET'])
def fetch_products_api(request):
    """API endpoint to fetch products with filters."""
    serializer = ProductFilterSerializer(data=request.GET)
    if not serializer.is_valid():
        return Response(serializer.errors, status=400)

    filters = serializer.validated_data
    products = ProductService.fetch_products(filters)
    print(products)
    return Response(ProductSerializer(products,many=True).data, status=200)