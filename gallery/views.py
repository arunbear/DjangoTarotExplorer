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

def wands(request):
    return render(request, 'gallery/suite.html', {'cards': gallery.models.wands})

def cups(request):
    return render(request, 'gallery/suite.html', {'cards': gallery.models.cups})

def swords(request):
    return render(request, 'gallery/suite.html', {'cards': gallery.models.swords})

def coins(request):
    return render(request, 'gallery/suite.html', {'cards': gallery.models.coins})

def trumps(request):
    return render(request, 'gallery/trumps.html', {'cards': gallery.models.trumps})

def trumps_in_pairs(request):
    return render(request, 'gallery/trumps.html', {'cards': gallery.models.trumps_in_pairs})

def about(request):
    return render(request, 'gallery/about.html')

def deal(request):
    context = {
        'images_json': gallery.models.all_cards_json,
        'back_of_card_img': 'https://upload.wikimedia.org/wikipedia/commons/f/fc/Waite%E2%80%93Smith_Tarot_Roses_and_Lilies_cropped.jpg'
    }
    return render(request, 'gallery/deal.html', context=context)