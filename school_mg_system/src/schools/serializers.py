from django.core.exceptions import ValidationError
from django.db import transaction
from rest_framework import serializers

from src.accounts.serializers import RegistrationSerializer
from src.schools.models import School
from src.libs.validators import validate_mail, validate_password


class SchoolSerializer(RegistrationSerializer):
    id = serializers.IntegerField(read_only=True)
    email = serializers.CharField(max_length=255)
    name = serializers.CharField(max_length=50)
    city = serializers.CharField(max_length=20)
    pincode = serializers.CharField(max_length=6)
    password = serializers.CharField(max_length=100, write_only=True)
    username = serializers.CharField(max_length=100, required=True)
    is_staff = serializers.BooleanField(read_only=True)

    class Meta:
        model = School
        fields = "__all__"

    def validate(self, data):
        validation_errors = {}
        email = data.get("email", None)
        if email and not validate_mail(email):
            validation_errors.update({"email": "Invalid email format."})

        password = data.get("password", None)
        if password and not validate_password(password):
            validation_errors.update(
                {"password": "Password entered didn't match the requirements."}
            )

        if validation_errors:
            raise ValidationError(validation_errors)

        return data

    @transaction.atomic
    def create(self, validated_data):
        try:
            password = validated_data.pop("password")
            username = validated_data.pop("username")
            user = super().create(
                is_staff=True,
                **{"password": password, "username": username, **validated_data},
            )
            school = School.objects.create(**validated_data)
            school.user = user
            school.save()
        except Exception as e:
            raise serializers.ValidationError(f"Error occured during create: {e}")
        return school

    @transaction.atomic
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
