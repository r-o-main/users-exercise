from rest_framework import viewsets, pagination, filters
from django_filters import rest_framework as rest_framework_filters
from .models import User
from .serializer import UserSerializer


class CustomPagination(pagination.PageNumberPagination):
    """ Pagination """
    page_query_param = 'page'
    page_size_query_param = 'page_size'
    page_size = 10
    max_page_size = 20


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be **viewed** or **edited**.
    """
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer
    pagination_class = CustomPagination
    filter_backends = (
        filters.SearchFilter,
        rest_framework_filters.DjangoFilterBackend,
        filters.OrderingFilter,
        )
    filterset_fields = ('last_name', 'first_name')
    search_fields = ['=last_name', 'email']
    ordering_fields = ['last_name', 'email']


class UserFilter(rest_framework_filters.FilterSet):
    """ Filterset """

    class Meta:
        model = User
        fields = ('last_name', 'first_name')
