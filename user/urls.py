from django.urls import path
from django.contrib.auth import views as auth_views

from user import views

app_name = "user"

urlpatterns = [
    path(
        "login",
        auth_views.LoginView.as_view(template_name="user/login.html"),
        name="login",
    ),
    path("logout", auth_views.LogoutView.as_view(), name="logout"),
    path("signup", views.signup, name="signup"),
    path("profile", views.profile, name="profile"),
]
