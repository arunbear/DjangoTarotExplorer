from collections import namedtuple
from django.shortcuts import render

UriPart = namedtuple("UriPart", ["prefix", "file"])

# Create your views here.
def index(request):
    uri_parts = [
        UriPart('1/11', 'Wands01.jpg'),
        UriPart('0/0f', 'Wands02.jpg'),
        UriPart('f/ff', 'Wands03.jpg'),
        UriPart('a/a4', 'Wands04.jpg'),
        UriPart('9/9d', 'Wands05.jpg'),
        UriPart('3/3b', 'Wands06.jpg'),
        UriPart('e/e4', 'Wands07.jpg'),
        UriPart('6/6b', 'Wands08.jpg'),
        UriPart('4/4d', 'Tarot_Nine_of_Wands.jpg'),
        UriPart('0/0b', 'Wands10.jpg'),
        UriPart('6/6a', 'Wands11.jpg'),
        UriPart('1/16', 'Wands12.jpg'),
        UriPart('0/0d', 'Wands13.jpg'),
        UriPart('c/ce', 'Wands14.jpg'),
    ]
    return render(request, 'gallery/index.html', context={'uri_parts': uri_parts})