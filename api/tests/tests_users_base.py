from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from rest_framework import status
from api.models import Users
from application.utils import encode_jwt

class UsersTestBase(TestCase):
    # Teste para a user viewset
    default_user_email = 'test@email.com'
    default_user_pass = 'pass'

    user_data = None
    access_token = None

    def setUp(self):
        # Cria um usuário default antes dos testes
        self.user_data = self.make_user()
        self.access_token = self.make_access_token({'id': str(self.user_data.pk), 'type': 'user'})
        

    def make_access_token(self, payload):
        return encode_jwt(payload, settings.APP_JWT_SECRET, expires_in=5)

    def make_user(self, email='test@email.com', name='Name', password='pass', birth_date='2000-01-01'):
        return Users.objects.create(
            email=email,
            name=name,
            password=make_password(password),
            birth_date=birth_date,
        )
