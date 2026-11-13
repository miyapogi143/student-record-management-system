from django.urls import path
from . import views
urlpatterns = [path("",views.enrollment_list,name="enrollment_list"),path("add/",views.enrollment_create,name="enrollment_create"),path("<int:pk>/edit/",views.enrollment_edit,name="enrollment_edit"),path("<int:pk>/delete/",views.enrollment_delete,name="enrollment_delete")]
