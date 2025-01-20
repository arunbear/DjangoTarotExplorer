from django.urls import path

from . import views

app_name = 'gallery'

urlpatterns = [
    path("", views.index, name="index"),
    path("royals/", views.royals, name="royals"),
]