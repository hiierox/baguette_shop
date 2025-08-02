from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet

router = DefaultRouter()
router.register(r'admin/orders', OrderViewSet, basename='admin-orders')


if router.registry:
    router.registry[0][1].admin_view = True  # [0][1] это сам ViewSet

urlpatterns = [
    path('user/<int:user_id>/orders/', OrderViewSet.as_view({'get': 'list'}), name='user-orders'),
    path('user/<int:user_id>/order/<int:pk>/', OrderViewSet.as_view({'get': 'retrieve'}), name='user-order'),
    path('', include(router.urls)),
]