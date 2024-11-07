from django.urls import path

from home import views

app_name = "home"

urlpatterns = [
    path("", views.splash, name="splash"),
    path("home", views.index, name="index"),
    path("projects", views.projects, name="projects"),
    # login/signup/logout
    # path("login", views.login, name="login"),
    # path("logout", views.logout, name="logout"),
    # path("signup", views.signup, name="signup"),
]
