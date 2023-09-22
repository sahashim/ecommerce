from rest_framework import serializers

from product.models import Product, Category, Brand


class BrandSerializer(serializers.ModelSerializer):
    """
    The brand model serializer.
    """

    class Meta:
        model = Brand
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    """
    The product model serializer.
    """

    class Meta:
        model = Product
        fields = '__all__'

    brands = BrandSerializer(read_only=True, source='brand')


class CategorySerializer(serializers.ModelSerializer):
    """
    The category model serializer.
    """

    class Meta:
        model = Category
        # exclude = ()
