from django.urls import path
from src.students.views import StudentBulkView, StudentListView, StudentView

urlpatterns = [
    path("get-or-add", StudentListView.as_view(), name="student"),
    path("update/<int:pk>/", StudentView.as_view(), name="update_student"),
    path("add-bulk", StudentBulkView.as_view(), name="add_bulk_students"),
]
