from collections import namedtuple

from django.db import models

# Create your models here.
UriParts = namedtuple("UriParts", ["wands", "cups", "swords"], defaults=[[], [], []])
UriPart  = namedtuple("UriPart", ["prefix", "file"])

uri_parts = UriParts(
    wands = [
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
    ],
    cups = [
        UriPart('3/36', 'Cups01.jpg'),
        UriPart('f/f8', 'Cups02.jpg'),
        UriPart('7/7a', 'Cups03.jpg'),
        UriPart('3/35', 'Cups04.jpg'),
        UriPart('d/d7', 'Cups05.jpg'),
        UriPart('1/17', 'Cups06.jpg'),
        UriPart('a/ae', 'Cups07.jpg'),
        UriPart('6/60', 'Cups08.jpg'),
        UriPart('2/24', 'Cups09.jpg'),
        UriPart('8/84', 'Cups10.jpg'),
        UriPart('a/ad', 'Cups11.jpg'),
        UriPart('f/fa', 'Cups12.jpg'),
        UriPart('6/62', 'Cups13.jpg'),
        UriPart('0/04', 'Cups14.jpg'),
    ],
    swords = [
        UriPart('1/1a', 'Swords01.jpg'),
        UriPart('9/9e', 'Swords02.jpg'),
        UriPart('0/02', 'Swords03.jpg'),
        UriPart('b/bf', 'Swords04.jpg'),
        UriPart('2/23', 'Swords05.jpg'),
        UriPart('2/29', 'Swords06.jpg'),
        UriPart('3/34', 'Swords07.jpg'),
        UriPart('a/a7', 'Swords08.jpg'),
        UriPart('2/2f', 'Swords09.jpg'),
        UriPart('d/d4', 'Swords10.jpg'),
        UriPart('4/4c', 'Swords11.jpg'),
        UriPart('b/b0', 'Swords12.jpg'),
        UriPart('d/d4', 'Swords13.jpg'),
        UriPart('3/33', 'Swords14.jpg'),
    ]
)
