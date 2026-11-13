from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from records import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("accounts/logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("", views.dashboard, name="dashboard"),
    path("students/", include("records.student_urls")),
    path("courses/", include("records.course_urls")),
    path("enrollments/", include("records.enrollment_urls")),
    path("reports/export/", views.export_students_csv, name="export_students"),
]
