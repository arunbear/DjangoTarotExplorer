from django.shortcuts import render

import gallery
from gallery.models import deck


# Create your views here.
def index(request):
    return render(request, 'gallery/index.html', context={'deck': deck})

def royals(request):
    return render(request, 'gallery/royals.html', { 'cards': gallery.models.royals.by_suite })


