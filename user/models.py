from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.validators import RegexValidator
from django.db import models

class CustomUser(AbstractUser):
    phone_regex = RegexValidator(
        regex=r'^010-\d{4}-\d{4}$',
        message="전화번호는 010-0000-0000 형식으로 입력해주세요."
    )
    phone_number = models.CharField(max_length=13, validators=[phone_regex])
    nickname = models.CharField(max_length=20, unique=True)

    groups=models.ManyToManyField(Group, related_name="customuser_set", blank=True)
    user_permissions=models.ManyToManyField(Permission, related_name="customuser_permissions_set", blank=True)