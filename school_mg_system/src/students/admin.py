from django.contrib import admin

from .models import Student

# Register your models here.
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    model = Student
    list_display = ["name", "get_username", "school", "grade"]
    list_filter = ["school", "grade"]

    @admin.display(description="Username")
    def get_username(self, obj):
        return getattr(getattr(obj, "user", None), "username", None)
