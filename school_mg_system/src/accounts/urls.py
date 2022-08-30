from django.urls import path, include

from rest_framework_simplejwt.views import TokenObtainPairView

from .views import RegistrationView

urlpatterns = [
    path("signin/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("signin/refresh/", TokenObtainPairView.as_view(), name="token_refresh"),
    path("register", RegistrationView.as_view()),
]
