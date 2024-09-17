from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from datetime import datetime


class MyUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, username, password, **extra_fields)
    
    
class User(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    
    USER_ROLES = [
        ('admin', 'NurseAdmin'),
        ('nurse', 'Nurse'),
        ('chp', 'Community Health Promoter'),
    ]
    
    user_role = models.CharField(
        max_length=50, 
        choices=USER_ROLES, 
        blank=True, 
        null=True
    )
    
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(default=datetime.now)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    objects = MyUserManager()
    
    def __str__(self):
        return self.username
    
    



