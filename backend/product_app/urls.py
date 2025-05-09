from django.contrib import admin
from django.urls import path
from django.http import HttpResponse
from .views import ProductListCreateView,ProductDetailView, ProductCategoryListCreateView, ProductByCategoryView, ProductCategoryListCreateView, ProductManageByCategoryView, fetch_products_api,product_list
def hello_world(request):
    return HttpResponse("Hello, world! This is our interneers-lab Django server. THis has been edited")


from django.contrib import admin
from django.urls import path
from django.http import JsonResponse

def hello_name(request):
    """
    A simple view that returns 'Hello, {name}' in JSON format.
    Uses a query parameter named 'name'.
    """
    # Get 'name' from the query string, default to 'World' if missing
    name = request.GET.get("name", "World")
    return JsonResponse({"message": f"Hello, {name}!"})


urlpatterns = [
    path('', product_list, name='product_list'),
    path('d/<str:product_id>/', ProductDetailView.as_view(), name='product-detail'),
    path('cat/', ProductCategoryListCreateView.as_view(), name='category-list-create'),
    path('cat/<str:category_id>', ProductByCategoryView.as_view(), name='products-by-category'),
    path('cat/<str:category_id>/p/<str:product_id>', ProductManageByCategoryView.as_view(), name='products-by-category'),
    path('filter/', fetch_products_api, name='fetch'),
    path('list/', ProductListCreateView.as_view(), name='product_list_view'),
]
