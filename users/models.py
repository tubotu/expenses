from django.db import models 
from django.contrib.auth.models import PermissionsMixin 
from django.contrib.auth.base_user import AbstractBaseUser 
from django.utils import timezone
from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
    """カスタムユーザーマネージャー"""
    use_in_migrations = True
    def _create_user(self, user_name, password, **extra_fields):
        # user_name を必須にする
        if not user_name:
            raise ValueError('The given user_name must be set')
        # user_name で User モデルを作成
        user = self.model(user_name=user_name, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user
    def create_user(self, user_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(user_name, password, **extra_fields)
    def create_superuser(self, user_name, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')
        return self._create_user(user_name, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    """カスタムユーザーモデル"""     
    user_name = models.CharField(max_length=15, unique=True, null=False)
    is_staff = models.BooleanField("is_staff", default=False)
    is_active = models.BooleanField("is_active", default=True)     
    date_joined = models.DateTimeField("date_joined", default=timezone.now) 
 
    objects = UserManager() 
 
    USERNAME_FIELD = "user_name"     
    REQUIRED_FIELDS = [] 
 
    class Meta:         
        verbose_name = "user"
        verbose_name_plural = "users"