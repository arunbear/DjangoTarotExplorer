from django.shortcuts import render

from gallery.models import deck

# Create your views here.
def index(request):
    return render(request, 'gallery/index.html', context={'deck': deck})

def royals(request):
    context = {
      'wands_and_cups'  : [*deck.wands[10:14],  *deck.cups[13:9:-1]],
      'swords_and_coins': [*deck.swords[10:14], *deck.coins[13:9:-1]]
    }
    return render(request, 'gallery/royals.html', context=context)


