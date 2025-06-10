from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from django_filters import rest_framework as filters
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer


class StandardResultSerPagination(PageNumberPagination):
    page_size = 10
    page_query_param = 'page'
    max_page_size = 50


class ProductFilter(filters.Filter):
    material = filters.MultipleChoiceFilter(
        field_name='material',
        lookup_expr='in',
        # вот эта штука сразу запрос делает в бд так что если табилц еще нет то не даст сделать миграции
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
    stock_gte = filters.NumberFilter(field_name='stock', lookup_expr='gte')

    class Meta:
        model = Product
        fields = ['material', 'price', 'width', 'height', 'categories', 'stock']


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    http_method_names = ['get']
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = ['material', 'price', 'width', 'height', 'categories', 'stock']
    pagination_class = StandardResultSerPagination
    lookup_field = 'slug'

    def list(self, request, *args, **kwargs):
        if request.path == '/product/':  # здесь product/ потому что без pk он тоже в list направится
            return Response({"detail": f"Redirect to {request.get_host()}/products/"}, status=400)
        return super().list(request, *args, **kwargs)  # ViewSet.list уже возвращает Response
