from rest_framework import serializers
from django.conf import settings
from .models import Users
from application.utils import encode_jwt

class UsersSerializer(serializers.ModelSerializer):
    access_token = serializers.SerializerMethodField()
    class Meta:
        model = Users
        fields = [
            'id','name','email','birth_date', 'access_token',
            'created_at','updated_at',
        ]

    def get_access_token(self, obj):
        if (self.context.get('get_jwt', False)):
            payload = { 'id': str(obj.id), 'type': 'p' }
            return encode_jwt(payload, settings.APP_JWT_SECRET, expires_in = 21600)
        else:
            return None