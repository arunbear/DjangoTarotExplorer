from dataclasses import dataclass
from typing import NamedTuple

# Create your models here.

@dataclass(frozen=True)
class Card:
    uri_key: str
    file: str

@dataclass(frozen=True)
class Deck:
    wands: list[Card]
    cups: list[Card]
    swords: list[Card]
    coins: list[Card]
    majors1: list[Card]
    majors2: list[Card]

    def all_cards(self) -> list[Card]:
        return [ *self.wands, *self.cups, *self.swords, *self.coins, *self.majors1, *self.majors2 ]

    def pips(self) -> list[Card]:
        pips = []
        for i in range(0, 10):
            pips.extend([deck.wands[i], deck.cups[i], deck.swords[i], deck.coins[i]])

        return pips

class RoyalGrouping(NamedTuple):
    wands: list[Card]
    cups: list[Card]
    swords: list[Card]
    coins: list[Card]
    by_suite: list[Card]
    by_rank: list[Card]

deck = Deck(
    wands = [
        Card('1/11', 'Wands01.jpg'),
        Card('0/0f', 'Wands02.jpg'),
        Card('f/ff', 'Wands03.jpg'),
        Card('a/a4', 'Wands04.jpg'),
        Card('9/9d', 'Wands05.jpg'),
        Card('3/3b', 'Wands06.jpg'),
        Card('e/e4', 'Wands07.jpg'),
        Card('6/6b', 'Wands08.jpg'),
        Card('4/4d', 'Tarot_Nine_of_Wands.jpg'),
        Card('0/0b', 'Wands10.jpg'),
        Card('6/6a', 'Wands11.jpg'),
        Card('1/16', 'Wands12.jpg'),
        Card('0/0d', 'Wands13.jpg'),
        Card('c/ce', 'Wands14.jpg'),
    ],
    cups = [
        Card('3/36', 'Cups01.jpg'),
        Card('f/f8', 'Cups02.jpg'),
        Card('7/7a', 'Cups03.jpg'),
        Card('3/35', 'Cups04.jpg'),
        Card('d/d7', 'Cups05.jpg'),
        Card('1/17', 'Cups06.jpg'),
        Card('a/ae', 'Cups07.jpg'),
        Card('6/60', 'Cups08.jpg'),
        Card('2/24', 'Cups09.jpg'),
        Card('8/84', 'Cups10.jpg'),
        Card('a/ad', 'Cups11.jpg'),
        Card('f/fa', 'Cups12.jpg'),
        Card('6/62', 'Cups13.jpg'),
        Card('0/04', 'Cups14.jpg'),
    ],
    swords = [
        Card('1/1a', 'Swords01.jpg'),
        Card('9/9e', 'Swords02.jpg'),
        Card('0/02', 'Swords03.jpg'),
        Card('b/bf', 'Swords04.jpg'),
        Card('2/23', 'Swords05.jpg'),
        Card('2/29', 'Swords06.jpg'),
        Card('3/34', 'Swords07.jpg'),
        Card('a/a7', 'Swords08.jpg'),
        Card('2/2f', 'Swords09.jpg'),
        Card('d/d4', 'Swords10.jpg'),
        Card('4/4c', 'Swords11.jpg'),
        Card('b/b0', 'Swords12.jpg'),
        Card('d/d4', 'Swords13.jpg'),
        Card('3/33', 'Swords14.jpg'),
    ],
    coins = [
        Card('f/fd', 'Pents01.jpg'),
        Card('9/9f', 'Pents02.jpg'),
        Card('4/42', 'Pents03.jpg'),
        Card('3/35', 'Pents04.jpg'),
        Card('9/96', 'Pents05.jpg'),
        Card('a/a6', 'Pents06.jpg'),
        Card('6/6a', 'Pents07.jpg'),
        Card('4/49', 'Pents08.jpg'),
        Card('f/f0', 'Pents09.jpg'),
        Card('4/42', 'Pents10.jpg'),
        Card('e/ec', 'Pents11.jpg'),
        Card('d/d5', 'Pents12.jpg'),
        Card('8/88', 'Pents13.jpg'),
        Card('1/1c', 'Pents14.jpg'),
    ],
    majors1= [
        Card('9/90', 'RWS_Tarot_00_Fool.jpg'),
        Card('d/de', 'RWS_Tarot_01_Magician.jpg'),
        Card('8/88', 'RWS_Tarot_02_High_Priestess.jpg'),
        Card('d/d2', 'RWS_Tarot_03_Empress.jpg'),
        Card('c/c3', 'RWS_Tarot_04_Emperor.jpg'),
        Card('8/8d', 'RWS_Tarot_05_Hierophant.jpg'),
        Card('d/db', 'RWS_Tarot_06_Lovers.jpg'),
        Card('9/9b', 'RWS_Tarot_07_Chariot.jpg'),
        Card('f/f5', 'RWS_Tarot_08_Strength.jpg'),
        Card('4/4d', 'RWS_Tarot_09_Hermit.jpg'),
        Card('3/3c', 'RWS_Tarot_10_Wheel_of_Fortune.jpg'),
    ],
    majors2= [
        Card('e/e0', 'RWS_Tarot_11_Justice.jpg'),
        Card('2/2b', 'RWS_Tarot_12_Hanged_Man.jpg'),
        Card('d/d7', 'RWS_Tarot_13_Death.jpg'),
        Card('f/f8', 'RWS_Tarot_14_Temperance.jpg'),
        Card('5/55', 'RWS_Tarot_15_Devil.jpg'),
        Card('5/53', 'RWS_Tarot_16_Tower.jpg'),
        Card('d/db', 'RWS_Tarot_17_Star.jpg'),
        Card('7/7f', 'RWS_Tarot_18_Moon.jpg'),
        Card('1/17', 'RWS_Tarot_19_Sun.jpg'),
        Card('d/dd', 'RWS_Tarot_20_Judgement.jpg'),
        Card('f/ff', 'RWS_Tarot_21_World.jpg'),
    ]
)

def __royals_by_rank():
    cards = []
    for i in range(10, 14):
        cards.extend([deck.wands[i], deck.cups[i], deck.swords[i], deck.coins[i]])
    return cards

royals = RoyalGrouping(
    wands  = [*deck.wands[10:14]],
    cups   = [*deck.cups[10:14]],
    swords = [*deck.swords[10:14]],
    coins  = [*deck.coins[10:14]],
    by_rank= __royals_by_rank(),
    by_suite=[*deck.wands[10:14], *deck.cups[10:14], *deck.swords[10:14], *deck.coins[10:14]],
)

def wands():
    return deck.wands

def cups():
    return deck.cups

def swords():
    return deck.swords

def coins():
    return deck.coins