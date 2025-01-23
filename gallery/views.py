from django.shortcuts import render

import gallery
from gallery.models import deck


# Create your views here.
def index(request):
    return render(request, 'gallery/index.html', context={'cards': deck.all_cards()})

def pips(request):
    return render(request, 'gallery/4_col_grid.html', context={'cards': deck.pips()})

def royals(request):
    return render(request, 'gallery/4_col_grid.html', {'cards': gallery.models.royals.by_suite})

def royals_by_rank(request):
    return render(request, 'gallery/4_col_grid.html', {'cards': gallery.models.royals.by_rank})