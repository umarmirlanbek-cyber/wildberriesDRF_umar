from .models import Product,Category,SubCategory
from modeltranslation.translator import TranslationOptions,register

@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('category_name',)

@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ('product_name','description')

@register(SubCategory)
class SubCategoryTranslationOptions(TranslationOptions):
    fields = ('subcategory_name',)