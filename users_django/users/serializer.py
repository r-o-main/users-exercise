from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    """ ModelSerializer is a shortcut class for automatically create serializers based on a given model class.

        This serializer handles the serialization/deserialization of User data model instances,
        and their validation. The identity url of the object user is added.

        NB: address is redefined to allow a blank value.
    """

    url = serializers.HyperlinkedIdentityField(view_name='v1:user-detail')

    address = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=300,
        style={'base_template': 'textarea.html'})


    class Meta:
        model = User
        fields = ('url', 'id', 'first_name', 'last_name', 'email', 'password', 'address')
