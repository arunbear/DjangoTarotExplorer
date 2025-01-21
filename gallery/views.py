from django.shortcuts import render

import gallery
from gallery.models import deck


# Create your views here.
def index(request):
    return render(request, 'gallery/index.html', context={'deck': deck})

def royals(request):
    context = {
      'wands_and_cups'  : gallery.models.royals.wands_and_cups,
      'swords_and_coins': gallery.models.royals.swords_and_coins,
    }
    return render(request, 'gallery/royals.html', context=context)


