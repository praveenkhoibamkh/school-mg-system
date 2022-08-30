from django.http import Http404

from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from src.schools.models import School
from src.schools.serializers import SchoolSerializer
from src.libs.permissions import IsSchool


class SchoolListView(ListCreateAPIView):
    serializer_class = SchoolSerializer
    queryset = School.objects.all()

    def get_queryset(self):
        return super().get_queryset()

    def get(self, request, *args, **kwargs):
        try:
            user = self.context["request"].user
            schools = School.objects.filter(user=user)
            serializer = SchoolSerializer(schools, many=True)
            return Response({"schools": serializer.data})
        except Exception:
            raise Http404

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class SchoolView(APIView):
    permission_classes = [IsSchool]

    def get_object(self, pk):
        try:
            return School.objects.get(pk=pk)
        except School.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        school = self.get_object(pk)
        serializer = SchoolSerializer(school)
        return Response(serializer.data)
