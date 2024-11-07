from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render

urlpatterns = [
    # Admin url
    path("admin/", admin.site.urls),
    # Home page
    path("", include("home.urls")),
    # User app url
]

handler400 = "core.exceptions.bad_request"
handler404 = "core.exceptions.page_not_found"
handler500 = "core.exceptions.server_error"
