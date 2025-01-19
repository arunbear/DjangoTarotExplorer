from django.shortcuts import render

from gallery.models import deck

# Create your views here.
def index(request):
    return render(request, 'gallery/index.html', context={'uri_parts': deck})