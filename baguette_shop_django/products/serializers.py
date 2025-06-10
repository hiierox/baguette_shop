from rest_framework import serializers
from .models import Product, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class ProductSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    category_ids = serializers.ListField(child=serializers.IntegerField(), write_only=True, required=False)

    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'description', 'price', 'material', 'width', 'height', 'image', 'categories',
                  'stock', 'category_ids']
        read_only_fields = ['id']

    def create(self, validated_data):
        category_ids = validated_data.pop('category_ids', [])
        product = Product.objects.create(**validated_data)
        if category_ids:
            product.categories.set(category_ids)
        return product

    def update(self, instance, validated_data):
        category_ids = validated_data.pop('category_ids', [])
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.price = validated_data.get('price', instance.price)
        instance.material = validated_data.get('material', instance.material)
        instance.width = validated_data.get('width', instance.width)
        instance.height = validated_data.get('height', instance.height)
        # image обновляется автоматически через validated_data
        instance.stock = validated_data.get('stock', instance.stock)
        instance.save()
        if category_ids:
            instance.categories.set(category_ids)
        return instance
