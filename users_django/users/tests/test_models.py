from django.test import TestCase
from ..models import User


class UserTest(TestCase):
    """ Test module for User model """

    def setUp(self):
        self.serge = User.objects.create(
            first_name='Serge', last_name='Karamazov', email='skaramazov@ricardo.ch')
        self.odile = User.objects.create(
            first_name='Odile', last_name='Deray', email='oderay@ricardo.ch')


    def test_retrieve_user_when_by_last_name_should_match(self):
        '''Ensure users can be found by last name.
        '''
        user_serge_karamazov = User.objects.get(last_name='Karamazov')
        self.assertEqual(
            user_serge_karamazov.id, self.serge.id)


    def test_retrieve_user_when_by_name_should_match(self):
        '''Ensure users can be found by full name.
        '''
        user_serge_karamazov = User.objects.get(last_name='Karamazov', first_name='Serge')
        self.assertEqual(
            user_serge_karamazov.id, self.serge.id)


    def test_retrieve_user_when_by_email_should_match(self):
        '''Ensure users can be found by email.
        '''
        user_odile_deray = User.objects.get(email='oderay@ricardo.ch')
        self.assertEqual(
            user_odile_deray.id, self.odile.id)
