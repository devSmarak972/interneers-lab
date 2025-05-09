from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ProductSerializer, ProductCategorySerializer, ProductFilterSerializer
from .pagination import ProductPagination
from .services import ProductService, ProductCategoryService
from .repository import ProductRepository, ProductCategoryRepository
from rest_framework.generics import ListAPIView
from rest_framework.decorators import api_view
from django.http import JsonResponse
from .models import Product

# Instantiate repositories and services
product_repository = ProductRepository()
category_repository = ProductCategoryRepository()
product_service = ProductService(product_repository=product_repository, category_repository=category_repository)
category_service = ProductCategoryService(category_repository=category_repository)

class ProductListCreateView(ListAPIView):
    serializer_class = ProductSerializer
    pagination_class = ProductPagination

    def get_queryset(self):
        return product_service.list_products()

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            try:
                category_data = request.data.get('category')
                if category_data:
                    category = category_service.get_category(category_data.get('id'))
                    if not category:
                        category = category_service.create_category(category_data)
                
                product = product_service.create_product(serializer.validated_data)
                if category:
                    product = product_service.add_product_to_category(product.id, category.id)
                return Response(ProductSerializer(product).data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": "Failed to create product", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({"error": "Validation failed", "details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class ProductDetailView(APIView):
    serializer_class = ProductSerializer

    def get(self, request, product_id):
        product = product_service.get_product(product_id)
        if product:
            return Response(ProductSerializer(product).data, status=status.HTTP_200_OK)
        return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, product_id):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            try:
                category_data = request.data.get('category')
                
                # If category data is provided
                if category_data:
                    # Check if category exists
                    print(category_data,"in edit product")
                    category = category_service.get_category(category_data.get('id'))
                    # If category doesn't exist, create it
                    if not category:
                        category = category_service.create_category({
                            'title': category_data.get('title', category_data.get('name')),
                            'description': category_data.get('description', '')
                        })
                    
                    # Add product to category
                    product = product_service.add_product_to_category(product_id, category.id)
                    if not product:
                        return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
                
                product = product_service.update_product(product_id, serializer.validated_data)
                if product:
                    return Response(ProductSerializer(product).data, status=status.HTTP_200_OK)
                return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({"error": "Failed to update product", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({"error": "Validation failed", "details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, product_id):
        try:
            if product_service.delete_product(product_id):
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
        categories = category_service.list_categories()
        return Response(ProductCategorySerializer(categories, many=True).data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ProductCategorySerializer(data=request.data)
        if serializer.is_valid():
            try:
                category = category_service.create_category(serializer.validated_data)
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
        products = product_service.get_products_by_category(category_id)
        return Response(ProductSerializer(products, many=True).data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Create or update a product category.
        """
        serializer = ProductCategorySerializer(data=request.data)

        if serializer.is_valid():
            category = category_service.create_or_update_category(serializer.validated_data)
            if category:
                return Response(ProductCategorySerializer(category).data, status=status.HTTP_200_OK)
            return Response({"error": "Category not found."}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, category_id):
        """
        Delete a category and update associated products to 'Uncategorized'.
        """
        success = category_service.delete_category(category_id)

        if success:
            return Response({"message": "Category deleted, products reassigned."}, status=status.HTTP_200_OK)
        return Response({"error": "Category not found."}, status=status.HTTP_404_NOT_FOUND)

class ProductManageByCategoryView(APIView):
    """
    API View to fetch products by category.
    """

    def post(self, request, category_id, product_id):
        product = product_service.add_product_to_category(product_id, category_id)
        if product:
            return Response(ProductSerializer(product).data, status=status.HTTP_200_OK)
        return Response({"error": "Invalid product or category"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, product_id):
        product = product_service.remove_product_from_category(product_id)
        if product:
            return Response(ProductSerializer(product).data, status=status.HTTP_200_OK)
        return Response({"error": "Product not found"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def fetch_products_api(request):
    """API endpoint to fetch products with filters."""
    serializer = ProductFilterSerializer(data=request.GET)
    if not serializer.is_valid():
        return Response(serializer.errors, status=400)

    filters = serializer.validated_data
    products = product_service.fetch_products(filters)
    return Response(ProductSerializer(products, many=True).data, status=200)

def product_list(request):
    return render(request, 'products/list.html')

def get_products(request):
    products = Product.objects.all()
    products_data = [{
        'id': str(product.id),
        'name': product.name,
        'description': product.description,
        'price': product.price,
        'brand': product.brand,
        'quantity': product.quantity,
        'category': str(product.category.id)
    } for product in products]
    return JsonResponse(products_data, safe=False)