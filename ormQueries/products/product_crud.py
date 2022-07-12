from unicodedata import category
from .models import Product
from django.db.models import Q
from django.db.models import Avg
from django.db.models import Max


class ProductCrud:
    @classmethod
    def get_all_products(cls):
        """Returns all Products"""
        return Product.objects.all()

    @classmethod
    def find_by_model(cls, model_name):
        """finds the matching product by model name"""
        return Product.objects.get(model=model_name)

    @classmethod
    def last_record(cls):
        """finds the last record inserted"""
        return Product.objects.last()

    @classmethod
    def by_rating(cls, score):
        """finds products by their rating"""
        return Product.objects.filter(rating=score)

    @classmethod
    def by_rating_range(cls, first_score, second_score):
        return Product.objects.filter(rating__range=(first_score, second_score))

    @classmethod
    def by_rating_and_color(cls, score, color):
        """finds products within a rating range"""
        return Product.objects.filter(Q(rating=score) & Q(color=color))

    @classmethod
    def by_rating_or_color(cls, score, color):
        """finds products by a rating or color value"""
        return Product.objects.filter(Q(rating=score) | Q(color=color))

    @classmethod
    def no_color_count(cls):
        """returns the count of products that have no color value"""
        return len(Product.objects.filter(color=None))
        # return Product.objects.filter(color=None).count() alt way

    @classmethod
    def below_price_or_above_rating(cls, price, score):
        """returns products below a price or above a rating"""
        return Product.objects.filter(Q(price_cents__lt=price) | Q(rating__gt=score))

    @classmethod
    def ordered_by_category_alphabetical_order_and_then_price_decending(cls):
        """returns products ordered by category alphabetical and decending price"""
        return Product.objects.order_by('category', '-price_cents')

    @classmethod
    def products_by_manufacturer_with_name_like(cls, name):
        """returns products made by manufacturers with names containing an input string"""
        return Product.objects.filter(manufacturer__contains=name)

    @classmethod
    def manufacturer_names_for_query(cls, name):
        """returns a list of manufacturer names that match query"""
        return Product.objects.filter(manufacturer__contains=name).values_list('manufacturer', flat=True)

    @classmethod
    def not_in_a_category(cls, ctg):
        """returns products that are not in a category"""
        return Product.objects.exclude(category=ctg)

    @classmethod
    def limited_not_in_a_category(cls, ctg, amount):
        """returns products that are not in a category up to a limit"""
        return Product.objects.exclude(category=ctg)[:amount]

    @classmethod
    def category_manufacturers(cls, name):
        """returns an array of manufacturers for a category"""
        return Product.objects.filter(category=name).values_list('manufacturer', flat=True)

    @classmethod
    def average_category_rating(cls, name):
        """returns the average"""
        return Product.objects.filter(category=name).aggregate(Avg('rating'))

    @classmethod
    def greatest_price(cls):
        """returns the highest price"""
        return Product.objects.aggregate(Max('price_cents'))

    @classmethod
    def longest_model_name(cls):
        """returns the id of the product with the longest model name"""
        return Product.objects.aggregate(Max(len('model')))
