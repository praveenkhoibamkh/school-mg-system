from urllib import request
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from rest_framework import serializers

from src.schools.models import School
from src.accounts.serializers import RegistrationSerializer
from src.students.models import Student
from src.libs.validators import validate_password


class StudentSerializer(RegistrationSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=50)
    username = serializers.CharField(max_length=100, required=True)
    password = serializers.CharField(max_length=100, write_only=True)

    class Meta:
        model = Student
        fields = "__all__"

    def validate(self, data):
        password = data.get("password", None)
        if password and not validate_password(password):
            raise ValidationError(
                {"password": "Password entered didn't match the requirements."}
            )
        return data

    @transaction.atomic
    def create(self, validated_data):
        school_user = self.context["request"].user
        try:
            school = School.objects.get(user=school_user)
            password = validated_data.pop("password")
            username = validated_data.pop("username")
            user = super().create(
                is_staff=False,
                **{"password": password, "username": username, **validated_data},
            )
            student = Student.objects.create(**{"school": school, **validated_data})
            student.user = user
            student.save()
        except Exception as e:
            raise serializers.ValidationError(f"Error occured during create: {e}")

        return student


class BulkCreateStudentsSerializer(serializers.ListSerializer):
    child = StudentSerializer()

    def validate(self, data):
        for single_data in data:
            password = single_data.get("password", None)
            if password and not validate_password(password):
                raise ValidationError(
                    {"password": "Password entered didn't match the requirements."}
                )
        return data

    def create(self, validated_data):
        result = []
        request = self.context["request"]
        school_user = request.user
        grade = request.query_params["grade"]

        school = School.objects.get(user=school_user)
        for attributes in validated_data:
            user = User(
                username=attributes["username"], password=attributes["password"]
            )
            user.save()
            result.append(
                Student(
                    name=attributes.get("name", None),
                    user=user,
                    school=school,
                    grade=grade,
                )
            )
        try:
            Student.objects.bulk_create(result)
        except IntegrityError as e:
            raise ValidationError(e)
        return result


class UpdateStudentSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=100)

    class Meta:
        model = Student
        fields = ("name", "password")

    def validate(self, data):
        password = data.get("password", None)
        if password and not validate_password(password):
            raise ValidationError(
                {"password": "Password entered didn't match the requirements."}
            )
        return data

    @transaction.atomic
    def update(self, instance, validated_data):
        try:
            user = self.context["request"].user
            instance_user = instance.user
            name = validated_data["name"]
            password = validated_data["password"]

            # Non-staff user can only update their account
            if not user.is_staff and user.pk != instance_user.pk:
                raise serializers.ValidationError(
                    {"authorize": "You dont have permission for this user."}
                )

            # Staff user can update only the students in their school
            if user.is_staff and instance.school.user != user:
                raise serializers.ValidationError(
                    {"authorize": "You dont have permission for this user."}
                )

            if name:
                instance.name = name
            if password:
                instance.password = password
                instance.user.set_password(password)
            instance.user.save()
            instance.save()
        except Exception as e:
            raise serializers.ValidationError(f"Error occured during create: {e}")

        return instance
