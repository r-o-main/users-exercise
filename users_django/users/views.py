from rest_framework import viewsets
from .models import User
from .serializer import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be **viewed** or **edited**.
    """
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer
