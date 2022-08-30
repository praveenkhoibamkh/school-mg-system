from django.db import models

from src.libs.mixins.models import BaseModel

# Create your models here.


class School(BaseModel):
    email = models.EmailField(max_length=255, unique=False, null=True, blank=True)
    name = models.CharField(max_length=50, blank=True, unique=False)
    city = models.CharField(max_length=20, blank=False)
    pincode = models.CharField(max_length=6, blank=False)

    def __str__(self) -> str:
        return self.name

    @property
    def username(self):
        return self.user.username

    @property
    def password(self):
        return self.user.password
