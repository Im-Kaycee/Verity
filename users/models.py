from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)  # Hash the password
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('voter', 'Voter'),
    ]

    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=255)  # Make sure it's large enough
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='voter')
    voterID = models.CharField(max_length=20, unique=True)
    wallet_address = models.CharField(max_length=42, unique=True, default='0xFF5687dd63d55b6B5990bD2ad27927d5b9DAA6c1')  # Add wallet address field
    
    # Additional fields required by AbstractBaseUser
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'  # Use username for authentication
    REQUIRED_FIELDS = ['password', 'role', 'voterID', 'wallet_address']  # Fields required for user creation

    def __str__(self):
        return self.username
