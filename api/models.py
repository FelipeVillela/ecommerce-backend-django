from django.db import models
import uuid
from django.contrib.auth.hashers import make_password

# Create your models here.
class Users(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    email = models.EmailField('Email', unique=True)
    password = models.CharField('password', max_length=255, null=True)
    birth_date = models.DateField('Data de nascimento')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    


