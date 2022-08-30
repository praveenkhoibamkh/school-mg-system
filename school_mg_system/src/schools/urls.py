from django.urls import path
from src.schools.views import SchoolView, SchoolListView

urlpatterns = [
    path("add", SchoolListView.as_view(), name="create_school"),
    path("get/<int:pk>", SchoolView.as_view(), name="retrieve_school"),
]
