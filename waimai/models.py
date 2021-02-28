from django.db import models
from django.contrib.auth.models import User

# 客户信息


class yonghuUser(models.Model):
    nickName = models.CharField(null=True, blank=True, max_length=50)
    belong = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, blank=True)

    def __int__(self):
        return self.id
