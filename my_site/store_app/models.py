from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import DateField
from phonenumber_field.modelfields import PhoneNumberField
from .pagination import ProductPagination,CategoryPagination

class UserProfile(AbstractUser):
    STATUS_CHOICES = (
    ('gold','gold'),
    ('silver','silver'),
    ('bronze','bronze'),
    ('basic','basic')
    )

    age = models.PositiveSmallIntegerField(validators=[MinValueValidator(16),
                                                       MaxValueValidator(70)],
                                           null=True,blank=True)
    phone_number = PhoneNumberField()
    status = models.CharField(max_length=32,choices=STATUS_CHOICES,default='basic')
    date_register = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class Category(models.Model):
    category_name = models.CharField(max_length=32,unique=True)
    category_image = models.ImageField(upload_to='photo_category/')
    pagination_class = CategoryPagination

    def __str__(self):
        return f'{self.category_name}'

class SubCategory(models.Model):
    subcategory_name = models.CharField(max_length=64,unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,related_name='category_sub')

    def __str__(self):
        return self.subcategory_name

class Product(models.Model):
    product_name = models.CharField(max_length=64)
    price = models.PositiveSmallIntegerField()
    description = models.TextField()
    subcategory = models.ForeignKey(SubCategory,on_delete=models.CASCADE)
    product_type = models.BooleanField()
    article = models.PositiveIntegerField(unique=True)
    video = models.FileField(null=True,blank=True)
    created_date = DateField(auto_now_add=True)
    pagination_class = ProductPagination

    def __str__(self):
        return f'{self.product_name} {self.price}'


    def get_avg_rating(self):
        rating = self.product_review.all()
        if rating.exists():
            return round(sum(i.star for i in rating) / rating.count(),2)
        return 0

    def get_count_people(self):
        return self.product_review.count()

class ProductImage(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='product_photo')
    product_image = models.ImageField(upload_to='photo_product')

    def __str__(self):
        return self.product.product_name


class Review(models.Model):
    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='product_review')
    star = models.PositiveSmallIntegerField(choices=[(i, str(i))for i in range(1,6)],
                                            null=True, blank=True)
    text = models.TextField(null=True,blank=True)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.product

class Cart(models.Model):
    user = models.OneToOneField(UserProfile,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user)

class Item(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE,related_name='items')
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.product} ,{self.quantity}'

    def get_total_price(self):
        return self.quantity * self.product.price
