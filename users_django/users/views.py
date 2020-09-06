from rest_framework import viewsets, pagination, filters, status
from rest_framework.response import Response
from django_filters import rest_framework as rest_framework_filters
from django.core import serializers
from .utils.iputils import get_originator_country_name_from
from .utils.decorator import push_to_kafka_upon_success
from .models import User
from .serializer import UserSerializer


class CustomPagination(pagination.PageNumberPagination):
    """ Class to handle the pagination:
        - use query parameter '?page=' to set the page in the url.
        - use query parameter '?page_size' to set the maximun number of users per page in the url.
    """
    page_query_param = 'page'
    page_size_query_param = 'page_size'
    page_size = 10
    max_page_size = 20

# The ModelViewSet provides the default actions:
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint for `list()`, `create()`, `retrieve()`, `update()`, `partial_update()` and `destroy()`actions
    on users.

    ### Endpoints:
    - [/api/v1/users](/api/v1/users): get all users (GET).
    - [/api/v1/users](/api/v1/users): create a new user (POST).
    - [/api/v1/users/:id](/api/v1/users/id): get user by id (GET).
    - [/api/v1/users/:id](/api/v1/users/id): partial update a user by id (PATCH).
    - [/api/v1/users/:id](/api/v1/users/id): update a user by id (PUT).
    - [/api/v1/users/:id](/api/v1/users/id): delete user by id (DELETE).

    ### Query parameters:

     - `last_name` to filter on last_name field.
     - `first_name` to filter on first_name field.
     - `search` to search in the last name and email fields.
     - `page` to set the page in the url.
     - `page_size` to set the maximun number of users per page in the url.

    For instance:
    `/api/v1/users/?last_name=Deray&first_name=Odile`
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


    @push_to_kafka_upon_success
    def create(self, request, *args, **kwargs):
        """
        Override parent create method to check whether the remote IP address is from Switzerland
        before creating the model instance.
        """
        originator_country = get_originator_country_name_from(request)
        if originator_country == 'Switzerland':
            response = super().create(request, *args, **kwargs)
            response.context_data = {'action': 'create', 'data': response.data}
            return response

        return Response(
            {
                'detail': f'Only users located in Switzerland can be created (remote address in {originator_country})',
            },
            status=status.HTTP_403_FORBIDDEN)


    @push_to_kafka_upon_success
    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        response.context_data = {'action': 'update', 'data': response.data}
        return response


    @push_to_kafka_upon_success
    def destroy(self, request, *args, **kwargs):
        user_to_delete = self.get_object()
        data_to_delete = serializers.serialize(format='json', queryset=[user_to_delete])

        response = super().destroy(request=request, *args, **kwargs)
        response.context_data = {
            'action': 'delete',
            'data': data_to_delete
        }
        return response


class UserFilter(rest_framework_filters.FilterSet):
    """ Class to filter  """

    class Meta:
        model = User
        fields = ('last_name', 'first_name')
