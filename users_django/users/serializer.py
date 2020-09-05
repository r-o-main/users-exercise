from rest_framework import serializers
from django.core.exceptions import ValidationError
from .models import User


class UserSerializer(serializers.ModelSerializer):
    """ ModelSerializer is a shortcut class for automatically create serializers based on a given model class.

        This serializer handles the serialization/deserialization of User data model instances,
        and their validation.

        NB: address is redefined to allow a blank value.
    """

    address = serializers.CharField(required=False, allow_blank=True, max_length=300)


    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'password', 'address')


    def validate(self, attrs):
        """ Override parent method to check that user is not already registered with the same email
            and raise a ValidationError exception if already used.
            :param attrs Dictionary of field values.

            NB: a user can have several accounts with different emails.
        """
        email_to_validate = attrs['email']
        if len(User.objects.filter(email=email_to_validate)) > 0:
            raise ValidationError(f"User {email_to_validate} is already used.")
        return attrs
