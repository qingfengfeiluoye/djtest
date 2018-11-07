from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class UserManager(BaseUserManager):
    def _create_user(self, telephone, username, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        user = self.model(username=username, telephone=telephone, **extra_fields)
        user.set_password(password)  # 密码加密
        user.save()
        return user

    def create_user(self, telephone, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(telephone, username, password, **extra_fields)

    def create_superuser(self, telephone, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(telephone, username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    telephone = models.CharField(max_length=11, unique=True)
    username = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    # 发邮件验证的指定字段
    EMAIL_FIELD = 'email'

    # form验证  authenticate(username=telephone,password=password)验证登录使用字段，创建超级用户的第一个字段
    USERNAME_FIELD = 'telephone'

    # 创建超级用户的中间字段，password字段为最后一个
    REQUIRED_FIELDS = ['username', 'email']

    objects = UserManager()
