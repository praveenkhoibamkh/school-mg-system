from django.http import Http404

from rest_framework.generics import CreateAPIView, ListCreateAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from src.schools.models import School
from src.students.models import Student
from src.libs.permissions import IsSchool
from src.students.serializers import (
    BulkCreateStudentsSerializer,
    StudentSerializer,
    UpdateStudentSerializer,
)

# Create your views here.
class StudentListView(ListCreateAPIView):
    serializer_class = StudentSerializer
    permission_classes = [IsSchool]
    queryset = Student.objects.all()

    def get_queryset(self):
        return super().get_queryset()

    def get(self, request, *args, **kwargs):
        try:
            grade = request.GET.get("grade", None)
            user = request.user
            school = School.objects.get(user=user)
            students = Student.objects.filter(school=school)

            if grade:
                # Add grade filter if included in param
                students = students.filter(grade=grade)

            serializer = StudentSerializer(students, many=True)
            return Response({"students": serializer.data})
        except Exception as e:
            raise Http404

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class StudentBulkView(CreateAPIView):
    serializer_class = BulkCreateStudentsSerializer
    permission_classes = [IsSchool]

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class StudentView(UpdateAPIView):
    serializer_class = UpdateStudentSerializer
    permission_classes = [IsAuthenticated]
    queryset = Student.objects.all()

    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)
