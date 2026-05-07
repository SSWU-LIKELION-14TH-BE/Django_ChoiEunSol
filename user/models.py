from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.validators import RegexValidator
from django.db import models
from django.conf import settings

class CustomUser(AbstractUser):
    phone_regex = RegexValidator(
        regex=r'^010-\d{4}-\d{4}$',
        message="전화번호는 010-0000-0000 형식으로 입력해주세요."
    )
    phone_number = models.CharField(max_length=13, validators=[phone_regex], default="010-0000-0000")
    nickname = models.CharField(max_length=20, null=True, blank=True)

    groups=models.ManyToManyField(Group, related_name="customuser_set", blank=True)
    user_permissions=models.ManyToManyField(Permission, related_name="customuser_permissions_set", blank=True)

class Guestbook(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='guestbooks'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='written_guestbooks'
    )

    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.author.nickname} → {self.owner.nickname}"