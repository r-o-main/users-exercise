from django.test import TestCase
from ..serializer import UserSerializer
from ..models import User


class TestUserSerializer(TestCase):


    def test_is_valid_when_all_attributes_are_filled_but_the_address_should_be_valid(self):
        valid_user_data = {
            'first_name': "Odile",
            'last_name': "Deray",
            'email': "oderay@ricardo.ch",
            'password': "0dIle_@98",
            'address': ""
            }
        serializer = UserSerializer(data=valid_user_data)
        self.assertTrue(serializer.is_valid(),
            msg=f"No validation errors should have been raised ({serializer.errors})")


    def test_is_valid_when_empty_last_name_should_be_invalid(self):
        user_data_without_last_name = {
            'first_name': "Odile",
            'last_name': "",
            'email': "oderay@ricardo.ch",
            'password': "0dIle_@98",
            'address': ""
            }
        serializer = UserSerializer(data=user_data_without_last_name)
        self.assertFalse(serializer.is_valid(), msg="last_name field may not be blank")
        self.assertTrue(len(serializer.errors['last_name']) > 0)


    def test_is_valid_when_empty_first_name_should_be_invalid(self):
        user_data_without_first_name = {
            'first_name': "",
            'last_name': "Deray",
            'email': "oderay@ricardo.ch",
            'password': "0dIle_@98",
            'address': ""
            }
        serializer = UserSerializer(data=user_data_without_first_name)
        self.assertFalse(serializer.is_valid(), msg="first_name field may not be blank")
        self.assertTrue(len(serializer.errors['first_name']) > 0)


    def test_is_valid_when_empty_email_should_be_invalid(self):
        user_data_without_email = {
            'first_name': "Odile",
            'last_name': "Deray",
            'email': "",
            'password': "0dIle_@98",
            'address': ""
            }
        serializer = UserSerializer(data=user_data_without_email)
        self.assertFalse(serializer.is_valid(), msg="email field may not be blank")
        self.assertTrue(len(serializer.errors['email']) > 0)


    def test_is_valid_when_invalid_email_format_should_be_invalid(self):
        user_data_without_email = {
            'first_name': "Odile",
            'last_name': "Deray",
            'email': "oderay_at_mail.com",
            'password': "0dIle_@98",
            'address': ""
            }
        serializer = UserSerializer(data=user_data_without_email)
        self.assertFalse(serializer.is_valid(), msg="email field is not a valid email address")
        self.assertTrue(len(serializer.errors['email']) > 0)


    def test_is_valid_when_empty_password_should_be_invalid(self):
        user_data_without_password = {
            'first_name': "Odile",
            'last_name': "Deray",
            'email': "oderay@ricardo.ch",
            'password': "",
            'address': ""
            }
        serializer = UserSerializer(data=user_data_without_password)
        self.assertFalse(serializer.is_valid(), msg="password field may not be blank")
        self.assertTrue(len(serializer.errors['password']) > 0)


    def test_is_valid_when_email_already_registered_should_be_invalid(self):
        odile = User.objects.create(
            first_name='Odile', last_name='Deray', email='oderay@ricardo.ch')
        valid_user_data = {
            'first_name': "Odile",
            'last_name': "Deray",
            'email': "oderay@ricardo.ch",
            'password': "0dIle_@98",
            'address': ""
            }
        serializer = UserSerializer(data=valid_user_data)
        self.assertFalse(serializer.is_valid(),
            msg=f"A validation error should have been raised as email [{odile.email}] is already used.")


    def test_is_valid_when_all_fields_but_email_have_meaningless_format_should_be_valid(self):
        user_data_bad_format = {
            'first_name': "4556",
            'last_name': "8_99",
            'email': "oderay@ricardo.ch",
            'password': "password",
            'address': "89445 121 545"
            }
        serializer = UserSerializer(data=user_data_bad_format)
        self.assertTrue(serializer.is_valid())


    def test_is_valid_when_all_fields_but_email_are_not_string_should_be_valid(self):
        user_data = {
            'first_name': 4556,
            'last_name': 99,
            'email': "oderay@ricardo.ch",
            'password': 4597,
            'address': 894451215
            }
        serializer = UserSerializer(data=user_data)
        self.assertTrue(serializer.is_valid())
