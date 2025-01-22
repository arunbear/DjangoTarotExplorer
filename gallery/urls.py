from django.urls import path

from . import views

app_name = 'gallery'

urlpatterns = [
    path("", views.index, name="index"),
    path("royals/", views.royals, name="royals"),
    path("royals/by/rank/", views.royals_by_rank, name="royals_by_rank"),
]