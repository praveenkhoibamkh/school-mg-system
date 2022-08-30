from django.contrib import admin

from src.schools.models import School

# Register your models here.
@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    model = School
    list_display = ["email", "get_username", "name", "city", "pincode"]

    @admin.display(description="Username")
    def get_username(self, obj):
        return getattr(getattr(obj, "user", None), "username", None)
