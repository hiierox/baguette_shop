from django.shortcuts import render
from rest_framework import viewsets, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.exceptions import PermissionDenied
from .models import User
from .serializers import UserSerializer
from .permissions import IsOwner


# по user/pk доступно (C)RUD, по user/ и users/ вызывается GET - list (user/pk GET-retrieve, роутер определяет)
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permission(self):
        if self.action in ['create', 'register']:
            return [AllowAny]
        if self.action == 'list':
            return [IsAdminUser()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsOwner()]
        return [IsAuthenticated()]

    def register(self, request, *args, **kwargs):
        return Response({'detail': 'all good let it register'}, status=200)

    def list(self, request, *args, **kwargs):
        if request.path == '/user/':  # здесь user/ потому что без pk он тоже в list направится
            if request.user.is_authenticated:
                return Response({"detail": f"Go to your profile: /user/{request.user.id}/"}, status=400)
            return Response({"detail": "Go to the homepage: /"}, status=400)
        elif not request.user.is_staff:
            return Response({"detail": "Only staff can see this, redirect to home"}, status=400)
        return Response(data=super().list(request, *args, **kwargs), status=200)
