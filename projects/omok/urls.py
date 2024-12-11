from django.urls import path

from projects.omok import views

app_name = "omok"

urlpatterns = [
    path("", views.index, name="index"),
]
