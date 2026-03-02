from .models import (Category,Product,SubCategory,UserProfile
,ProductImage,Review,Cart,Item)
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'password', 'age', 'phone_number')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','category_name','category_image']

class SubCategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['id','subcategory_name']

class SubCategoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['subcategory_name']

class CategoryDetailSerializer(serializers.ModelSerializer):
    category_sub = SubCategoryDetailSerializer(read_only=True,many=True)
    class Meta:
        model = Category
        fields = ['category_name','category_sub']

class ReviewSerializer(serializers.ModelSerializer):
    created_date = serializers.DateField(format='%d-%m-%Y')
    user = UserProfileSerializer()
    class Meta:
        model = Review
        fields = ['user','star','text','created_date']

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['product_image']

class ProductDetailSerializer(serializers.ModelSerializer):
    product_photo = ProductImageSerializer(read_only=True,many=True)
    avg_rating = serializers.SerializerMethodField()
    get_count_people = serializers.SerializerMethodField()
    product_review = ReviewSerializer(read_only=True,many=True)
    subcategory = SubCategoryListSerializer()
    class Meta:
        model = Product
        fields = ['id','subcategory','product_name','price','product_type','product_photo','avg_rating',
                  'get_count_people','article','description','product_review','video','created_date']

    def get_avg_rating(self, obj):
        return obj.get_avg_rating()

    def get_count_people(self,obj):
        return obj.get_count_people()

class ProductListSerializer(serializers.ModelSerializer):
    product_photo = ProductImageSerializer(read_only=True,many=True)
    avg_rating = serializers.SerializerMethodField()
    get_count_people = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = ['id','product_name','price','product_photo','avg_rating',
                  'get_count_people',]

    def get_avg_rating(self, obj):
        return obj.get_avg_rating()

    def get_count_people(self,obj):
        return obj.get_count_people()


class ItemSerializer(serializers.ModelSerializer):
    product = ProductListSerializer()
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all() ,
                                                    write_only=True,source='product')
    total_price = serializers.SerializerMethodField()
    class Meta:
        model = Item
        fields = ['id','product','product_id','quantity','total_price']

    def get_total_price(self,obj):
        return obj.get_total_price()

class CartSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True,read_only=True)
    class Meta:
        model = Cart
        fields = ['id','user','items']
        read_only_fields = ['user']