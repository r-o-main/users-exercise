from rest_framework import viewsets, pagination, filters, status
from rest_framework.response import Response
from django_filters import rest_framework as rest_framework_filters
from .iputils import get_originator_country_name_from
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


    def create(self, request, *args, **kwargs):
        """
        Override parent create method to check whether the remote IP address is from Switzerland
        before creating the model instance.
        """
        originator_country = get_originator_country_name_from(request)
        if originator_country == 'Switzerland':
            return super().create(request, *args, **kwargs)

        return Response(
            {'detail': f'Only users located in Switzerland can be created (remote address in {originator_country})'},
            status=status.HTTP_403_FORBIDDEN)


class UserFilter(rest_framework_filters.FilterSet):
    """ Filterset """

    class Meta:
        model = User
        fields = ('last_name', 'first_name')
