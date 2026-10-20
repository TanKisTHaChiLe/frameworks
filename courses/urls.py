from django.urls import path

from . import views


app_name = "courses"

urlpatterns = [
    path("", views.course_list, name="list"),
    path("statistics/", views.statistics, name="statistics"),
    path("<int:course_id>/", views.course_detail, name="detail"),
]
