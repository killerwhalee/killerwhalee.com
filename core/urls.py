from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Admin url
    path("admin/", admin.site.urls),
    # User applications
    path("", include("home.urls")),
    path("user/", include("user.urls")),
    path("projects/", include("projects.urls")),
]

handler400 = "core.exceptions.bad_request"
handler404 = "core.exceptions.page_not_found"
handler500 = "core.exceptions.server_error"
