from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from rest_framework import status
from api.models import Users
from application.utils import encode_jwt

class UsersViewSetTest(TestCase):
    # Teste para a user viewset
    default_user_email = 'test@email.com'
    default_user_pass = 'pass'

    user_data = None
    access_token = None

    def setUp(self):
        # Cria um usuário default antes dos testes
        self.user_data = Users.objects.create(
            email=self.default_user_email,
            name="Name",
            password=make_password(self.default_user_pass),
            birth_date='2000-09-23',
        )

        payload = { 'id': str(self.user_data.pk), 'type': 'user'}
        self.access_token = encode_jwt(payload, settings.APP_JWT_SECRET, expires_in=5)

    def test_api_create_user(self):
        url = reverse('api:users-list')
        body = {
            'email': 'test_create@email.com',
            'name': "Created",
            'password': '123456',
            'birth_date': '2000-01-01',
        }

        response = self.client.post(url, body)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_api_list_users(self):
        url = reverse('api:users-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_api_find_one_user_success(self):
        url = reverse('api:users-detail', kwargs={'pk': self.user_data.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_find_one_user_not_found(self):
        url = reverse('api:users-detail', kwargs={'pk': '123'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_api_user_login_success(self):
        url = reverse('api:users-login')
        body = {
            'email': self.default_user_email,
            'password': self.default_user_pass,
        }

        response = self.client.post(url, body)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_user_login_invalid_password(self):
        url = reverse('api:users-login')
        body = {
            'email': self.default_user_email,
            'password': '12345',
        }

        response = self.client.post(url, body)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_api_user_login_users_does_not_exists(self):
        url = reverse('api:users-login')
        body = {
            'email': 'nonexistent_user@email.com',
            'password': self.default_user_pass,
        }

        response = self.client.post(url, body)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_api_update_user(self):
        url = reverse('api:users-detail', kwargs={'pk': self.user_data.pk})
        response = self.client.put(url, headers={'Authorization': self.access_token})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_update_user(self):
        url = reverse('api:users-detail', kwargs={'pk': self.user_data.pk})
        headers = {
            'Authorization': self.access_token
        }
        body = {
            'email': f'updated@email.com',
            'name': f'Updated Name',
            'birth_date': '2000-01-01',
        }
        response = self.client.put(url, data=body, headers=headers, content_type='application/json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verfica se o usuário foi realmente atualizado
        updated_user = Users.objects.get(pk=self.user_data.pk)
        self.assertEqual(updated_user.email, body['email'])
        self.assertEqual(updated_user.name, body['name'])

    def test_api_partial_update_user(self):
        url = reverse('api:users-detail', kwargs={'pk': self.user_data.pk})
        headers = {
            'Authorization': self.access_token
        }
        body = {
            'name': f'{self.user_data.name} PartialUpdate',
        }
        response = self.client.patch(url, data=body, headers=headers, content_type='application/json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verfica se o usuário foi realmente atualizado
        updated_user = Users.objects.get(pk=self.user_data.pk)
        self.assertEqual(updated_user.name, body['name'])

    def test_api_delete_user(self):
        url = reverse('api:users-detail', kwargs={'pk': self.user_data.pk})
        headers = {
            'Authorization': self.access_token
        }
        response = self.client.delete(url, headers=headers, content_type='application/json')
        
        # Por enquanto método delete não está implementado
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
    