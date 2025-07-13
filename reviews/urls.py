from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, ReviewViewSet
from rest_framework_nested.routers import NestedDefaultRouter

from django.conf import settings
from django.conf.urls.static import static
from .views import product_detail_view

from .views import register_view, login_view, logout_view


router = DefaultRouter()
router.register(r'products', ProductViewSet)

product_router = NestedDefaultRouter(router, r'products', lookup='product')
product_router.register(r'reviews', ReviewViewSet, basename='product-reviews')


urlpatterns = [
    path('', include(router.urls)),
    path('', include(product_router.urls)),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('product/<int:pk>/', product_detail_view, name='product_detail'),

    
    
]




