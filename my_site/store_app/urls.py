from codecs import namereplace_errors

from rest_framework import routers
from .views import UserProfileViewSet, CartViewSet, CategoryListAPIView, CategoryDetailAPIView, ProductListAPIView,ProductDetailAPIView, SubCategoryListAPIView, SubCategoryDetailAPIView, ReviewViewSet, RegisterView, LoginView,LogoutView, ItemViewSet
from django.urls import path,include

router = routers.DefaultRouter()

router.register(r'user',UserProfileViewSet,basename='users')
router.register(r'userprofile',UserProfileViewSet,basename='userprofiles')
router.register(r'review',ReviewViewSet,basename='reviews')

urlpatterns = [
    path('',include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('product/',ProductListAPIView.as_view(),name='product_list'),
    path('product/<int:pk>',ProductDetailAPIView.as_view(),name='product_detail'),
    path('category/',CategoryListAPIView.as_view(),name='category_list'),
    path('category/<int:pk>',CategoryDetailAPIView.as_view(),name='category_detail'),
    path('subcategory/',SubCategoryListAPIView.as_view(),name='subcategory_list'),
    path('subcategory/<int:pk>',SubCategoryDetailAPIView.as_view(),name='subcategory_detail'),
    path('cart/', CartViewSet.as_view(), name='cart-items-list'),
    path('cart_items/',ItemViewSet.as_view({'get': 'list','post':'create'})),
    path('cart_items/<int:pk>', ItemViewSet.as_view({'put':'update','delete':'destroy'}),name='cart-items-detail'),
]