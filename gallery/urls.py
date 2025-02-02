from django.urls import path

from . import views

app_name = 'gallery'

urlpatterns = [
    path("all.html", views.index, name="index"),
    path("about.html", views.about, name="about"),
    path("trumps.html", views.trumps, name="trumps"),
    path("pips/by/number.html", views.pips, name="pips_by_number"),
    path("pips/cups.html", views.cups, name="cups"),
    path("pips/coins.html", views.coins, name="coins"),
    path("pips/swords.html", views.swords, name="swords"),
    path("pips/wands.html", views.wands, name="wands"),
    path("royals/by/suite.html", views.royals, name="royals_by_suite"),
    path("royals/by/rank.html", views.royals_by_rank, name="royals_by_rank"),
    path("deal.html", views.deal, name="deal"),
]