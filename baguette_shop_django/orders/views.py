from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from .models import Order
from .serializers import OrderSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

class IsOwnerOrAdminPermission(IsAuthenticated):
    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        return super().has_permission(request, view)

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return obj.user_id == request.user.id

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.prefetch_related('orderitem_set').all()
    serializer_class = OrderSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsOwnerOrAdminPermission]

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        if getattr(self, 'admin_view', False):
            return self.queryset.all()
        if user_id:
            return self.queryset.filter(user_id=user_id)
        return self.queryset.none()

    def retrieve(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')
        order_id = kwargs.get('pk')
        order = get_object_or_404(Order, id=order_id, user_id=user_id)
        self.check_object_permissions(request, order)
        return super().retrieve(request, *args, **kwargs)