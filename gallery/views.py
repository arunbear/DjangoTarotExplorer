from django.shortcuts import render

import gallery
from gallery.models import deck


# Create your views here.
def index(request):
    return render(request, 'gallery/index.html', context={'deck': deck})

def royals(request):
    context = {
      'wands' : gallery.models.royals.wands,
      'cups'  : gallery.models.royals.cups,
      'swords': gallery.models.royals.swords,
      'coins' :gallery.models.royals.coins,
    }
    return render(request, 'gallery/royals.html', context=context)


