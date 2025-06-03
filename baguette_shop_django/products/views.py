from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
# from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters
from .models import Product
from .serializers import ProductSerializer


class StandardResultSerPagination(PageNumberPagination):
    page_size = 20
    page_query_param = 'page_size'
    max_page_size = 50


class ProductFilter(filters.Filter):
    material = filters.MultipleChoiceFilter(
        field_name='material',
        lookup_expr='in',
        choices=[(material, material) for material in
                 Product.objects.values_list('material',
                                             flat=True).distinct()]
    )
    price_gte = filters.NumberFilter(field_name='price', lookup_expr='gte')
    price_lte = filters.NumberFilter(field_name='price', lookup_expr='lte')
    width_gte = filters.NumberFilter(field_name='width', lookup_expr='gte')
    width_lte = filters.NumberFilter(field_name='width', lookup_expr='lte')
    height_gte = filters.NumberFilter(field_name='height', lookup_expr='gte')
    height_lte = filters.NumberFilter(field_name='height', lookup_expr='lte')
    categories = filters.AllValuesMultipleFilter(field_name='categories')

    class Meta:
        model = Product
        fields = ['material', 'price', 'width', 'height', 'categories']


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    http_method_names = ['get']
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = []
    pagination_class = StandardResultSerPagination
