from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    """ ModelSerializer is a shortcut class for automatically create serializers based on a given model class.

        This serializer handles the serialization/deserialization of User data model instances,
        and their validation.

        NB: address is redefined to allow a blank value.
    """

    address = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=300,
        style={'base_template': 'textarea.html'})


    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'password', 'address')
