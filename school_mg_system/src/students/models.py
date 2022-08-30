from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

from src.schools.models import School
from src.libs.mixins.models import BaseModel

# Create your models here.


class Student(BaseModel):
    name = models.CharField(max_length=50, blank=True, unique=False)
    school = models.ForeignKey(School, on_delete=models.PROTECT, null=True)
    grade = models.IntegerField(
        default=1, validators=[MinValueValidator(1), MaxValueValidator(12)]
    )

    def __str__(self) -> str:
        return self.user.username

    @property
    def username(self):
        return self.user.username
