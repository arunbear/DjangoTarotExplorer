from django.urls import path

from . import views

app_name = 'gallery'

urlpatterns = [
    path("", views.index, name="index"),
    path("pips/by/number", views.pips, name="pips_by_number"),
    path("pips/cups/", views.cups, name="cups"),
    path("pips/coins/", views.coins, name="coins"),
    path("pips/swords/", views.swords, name="swords"),
    path("pips/wands/", views.wands, name="wands"),
    path("royals/by/suite/", views.royals, name="royals_by_suite"),
    path("royals/by/rank/", views.royals_by_rank, name="royals_by_rank"),
]