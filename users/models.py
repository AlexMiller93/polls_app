from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    city = models.CharField(max_length=20, blank=True, null=True)
    profession = models.CharField(max_length=50, blank=True, null=True)
    about = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['created']
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self) -> str:
        return self.user.username
