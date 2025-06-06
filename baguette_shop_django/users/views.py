from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response

from .models import User
from .permissions import IsOwner
from .serializers import UserSerializer


# по user/pk доступно (C)RUD, по user/ и users/ вызывается GET - list (user/pk GET-retrieve, роутер определяет)
# user/pk - retrieve
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    http_method_names = ['put', 'patch', 'delete', 'get']

    def get_permissions(self):
        if self.action == 'list':
            return [IsAdminUser()]
        elif self.action in ['update', 'partial_update', 'destroy', 'retrieve']:
            return [IsAuthenticated(), IsOwner()]
        return [IsAuthenticated()]


    def list(self, request, *args, **kwargs):
        if request.path == '/user/':  # здесь user/ потому что без pk он тоже в list направится
            if request.user.is_authenticated:
                return Response({"detail": f"Go to your profile: /user/{request.user.id}/"}, status=400)
            return Response({"detail": "Go to the homepage: /"}, status=400)
        elif not request.user.is_staff:
            return Response({"detail": "Only staff can see this, redirect to home"}, status=400)
        return super().list(request, *args, **kwargs)  # ViewSet.list уже возвращает Response