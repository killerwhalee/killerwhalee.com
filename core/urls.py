from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect, HttpResponse

urlpatterns = [
    # Admin page
    path("admin/", admin.site.urls),
    # Root url
    path("", lambda _: HttpResponse("Welcome to killerwhalee.com")),
    # User applications
]

handler400 = "core.exceptions.bad_request"
handler404 = "core.exceptions.page_not_found"
handler500 = "core.exceptions.server_error"
