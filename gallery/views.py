from django.shortcuts import render

import gallery
from gallery.models import deck


# Create your views here.
def index(request):
    return render(request, 'gallery/index.html', context={'cards': deck.all_cards()})

def royals(request):
    return render(request, 'gallery/royals.html', { 'cards': gallery.models.royals.by_suite })

def royals_by_rank(request):
    return render(request, 'gallery/royals.html', { 'cards': gallery.models.royals.by_rank })