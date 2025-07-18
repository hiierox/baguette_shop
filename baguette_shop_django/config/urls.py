"""
URL configuration for baguette_shop_django project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users.views import UserViewSet
from authentication.views import RegisterView, LoginView
from products.views import ProductViewSet
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenRefreshView

router = DefaultRouter()
router.register(r'user', UserViewSet)
router.register(r'product', ProductViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', RegisterView.as_view(), name="register"),
    path('login/', LoginView.as_view(), name='login'),
    path('', include(router.urls)),  # все маршруты приложений кроме списков - они ниже (products/, users/)
    path('users/', UserViewSet.as_view({'get': 'list'}), name='users_list'),
    path('products/', ProductViewSet.as_view({'get': 'list'}), name='products_list'),
    # api
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger_ui')
]
