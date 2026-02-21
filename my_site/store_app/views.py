from .models import (Category,UserProfile,SubCategory,
                     Product,ProductImage,Cart,Review,Item)
from .serializers import(UserProfileSerializer, CategoryListSerializer,CategoryDetailSerializer,
                          ProductListSerializer,ProductDetailSerializer,ReviewSerializer,LoginSerializer, CartSerializer, SubCategoryListSerializer,SubCategoryDetailSerializer,UserRegisterSerializer,ItemSerializer)
from rest_framework import viewsets,generics,permissions
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ProductFilter
from rest_framework.filters import SearchFilter,OrderingFilter
from .pagination import SubCategoryPagination,ProductPagination,CategoryPagination
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from tokenize import TokenError
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly


class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response({"detail": "Неверные учетные данные"}, status=status.HTTP_401_UNAUTHORIZED)

        user = serializer.validated_data
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if not refresh_token:
                return Response({'detail': 'Refresh токен не предоставлен.'}, status=status.HTTP_400_BAD_REQUEST)
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'detail': 'Вы успешно вышли.'}, status=status.HTTP_200_OK)
        except TokenError as e:
            return Response({'detail': 'Недействительный токен.'}, status=status.HTTP_400_BAD_REQUEST)


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def get_queryset(self):
        return UserProfile.objects.filter(id=self.request.user.id)

class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer
    pagination_class = CategoryPagination

class CategoryDetailAPIView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer

class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['product_name','article']
    ordering_fields = ['price','created_date']
    pagination_class = ProductPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

class SubCategoryListAPIView(generics.ListAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategoryListSerializer
    pagination_class = SubCategoryPagination

class SubCategoryDetailAPIView(generics.RetrieveAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategoryDetailSerializer

class CartViewSet(generics.RetrieveAPIView):
    serializer_class = CartSerializer

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = self.get_serializer(cart)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ItemViewSet(viewsets.ModelViewSet):
    serializer_class = ItemSerializer

    def get_queryset(self):
        return Item.objects.filter(cart__user=self.request.user)

    def perform_create(self, serializer):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        serializer.save(cart=cart)

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer