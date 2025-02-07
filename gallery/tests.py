from abc import ABCMeta, abstractmethod
from collections import namedtuple
from http import HTTPStatus

import bs4
from bs4 import BeautifulSoup
from django.test import TestCase
from django.urls import reverse

from gallery.models import deck

royals_by_suite = [
    deck.wands[10],  deck.wands[11],  deck.wands[12],  deck.wands[13],
    deck.cups[10],   deck.cups[11],   deck.cups[12],   deck.cups[13],
    deck.swords[10], deck.swords[11], deck.swords[12], deck.swords[13],
    deck.coins[10],  deck.coins[11],  deck.coins[12],  deck.coins[13],
]

royals_by_rank = [
    deck.wands[10], deck.cups[10], deck.swords[10], deck.coins[10],
    deck.wands[11], deck.cups[11], deck.swords[11], deck.coins[11],
    deck.wands[12], deck.cups[12], deck.swords[12], deck.coins[12],
    deck.wands[13], deck.cups[13], deck.swords[13], deck.coins[13],
]

class GalleryIndexViewSpecs(TestCase):

    def test_that_nav_bar_exists(self):
        response = self.client.get(reverse('gallery:index'))
        soup = BeautifulSoup(response.content, features="html.parser")
        navbar = soup.find("div", {"class": "navbar"})
        self.assertIsNotNone(navbar)

        links = navbar.select("a.toplink")
        self.check_about_link(links[0])
        self.assertEqual(links[0].text, "About")
        self.assertEqual("/gallery/about.html", links[0].get("href"))
        self.assertEqual(links[1].text, "All")
        self.assertEqual("/gallery/all.html", links[1].get("href"))

        self.check_dropdown_for_royals(navbar)
        self.check_dropdown_for_pips(navbar)
        self.assertEqual("Trumps", links[2].text)
        self.assertEqual("/gallery/trumps.html", links[2].get("href"))
        self.check_deal_link(links[3])

    def check_about_link(self, link: bs4.element.Tag):
        self.assertEqual(type(link), bs4.element.Tag)
        self.assertEqual(link.text, "About")

        expected_href = "/gallery/about.html"
        self.assertEqual(expected_href, link.get("href"))

        response = self.client.get(expected_href)
        self.assertEqual(HTTPStatus.OK, response.status_code)

    def check_dropdown_for_royals(self, navbar):
        dropdown = navbar.find("div", {"id": "dropdown-royals"})
        self.assertIsNotNone(dropdown)

        button = dropdown.find("button")
        self.assertRegex(button.text, "Royals")

        dropdown_content = dropdown.find("div", {"class": "dropdown-content"})
        dropdown_links = dropdown_content.select("a")
        self.assertEqual("By Suite", dropdown_links[0].text)
        self.assertEqual("/gallery/royals/by/suite.html", dropdown_links[0].get("href"))
        self.assertEqual("By Rank", dropdown_links[1].text)
        self.assertEqual("/gallery/royals/by/rank.html", dropdown_links[1].get("href"))

    def check_dropdown_for_pips(self, navbar):
        dropdown = navbar.find("div", {"id": "dropdown-pips"})
        self.assertIsNotNone(dropdown)
        button = dropdown.find("button")
        self.assertRegex(button.text, "Pips")

        dropdown_content = dropdown.find("div", {"class": "dropdown-content"})
        self.assertIsNotNone(dropdown_content)

        dropdown_links = dropdown_content.select("a")
        Link = namedtuple('Link', ['text', 'path'])
        expected_links = [
            Link("By Number", "/gallery/pips/by/number.html"),
            Link("Wands", "/gallery/pips/wands.html"),
            Link("Cups", "/gallery/pips/cups.html"),
            Link("Swords", "/gallery/pips/swords.html"),
            Link("Coins", "/gallery/pips/coins.html"),
        ]
        self.assertEqual(len(expected_links), len(dropdown_links))
        for expected_link, got_link in zip(expected_links, dropdown_links):
            with self.subTest():
                self.assertEqual(expected_link.text, got_link.text)
                self.assertEqual(expected_link.path, got_link.get("href"))

    def check_deal_link(self, link):
        self.assertEqual(link.text, "Deal")

        expected_href = "/gallery/deal.html"
        self.assertEqual(expected_href, link.get("href"))
        self.check_deal_page(expected_href)

    def check_deal_page(self, expected_href: str):
        response = self.client.get(expected_href)
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertTemplateUsed(response, "gallery/deal.html")

        soup = BeautifulSoup(response.content, features="html.parser")
        card_holder = soup.find("div", {"class": "card-holder"})
        self.assertIsNotNone(card_holder)

        cards = card_holder.select("img")
        self.assertEqual(len(cards), 3)

        button_holder = soup.find("div", {"class": "button-holder"})
        self.assertIsNotNone(button_holder)
        buttons = button_holder.select("button")
        self.assertEqual(len(buttons), 3)


class GridViewSpec:
    # Nest to prevent unittest from instantiating an ABC
    class CanViewAll(TestCase, metaclass=ABCMeta):
        def test_that_all_cards_can_can_be_viewed(self):
            response = self.client.get(self.page_uri())
            self.assertEqual(HTTPStatus.OK, response.status_code, f"{self.page_uri()} is OK")

            soup = BeautifulSoup(response.content, features="html.parser")
            grid = soup.find("div", {"class": "grid"})
            self.assertIsNotNone(grid)
            self.check_grid_contents(grid)

        def check_grid_contents(self, grid):
            links = grid.select("a")
            self.assertEqual(len(self.expected_cards()), self.expected_number_of_cards())
            self.assertEqual(len(links), self.expected_number_of_cards())

            for card, link in zip(self.expected_cards(), links):
                with self.subTest():
                    url = f"https://en.wikipedia.org/wiki/Rider%E2%80%93Waite_Tarot#/media/File:{card.file}"
                    self.assertEqual(url, link['href'])

                    img = link.find("img")
                    self.assertIsNotNone(img, f"Link contains an image")
                    img_src = f"https://upload.wikimedia.org/wikipedia/commons/{card.uri_key}/{card.file}"
                    self.assertEqual(img_src, img['src'])

        @abstractmethod
        def page_uri(self):
            pass

        @abstractmethod
        def expected_cards(self):
            pass

        @abstractmethod
        def expected_number_of_cards(self):
            pass


class CanViewAllDefaultGallery(GridViewSpec.CanViewAll):
    def expected_number_of_cards(self):
        return 78

    def page_uri(self):
        return reverse('gallery:index')

    def expected_cards(self):
        return deck.all_cards()

class CanViewAllRoyalsBySuite(GridViewSpec.CanViewAll):
    def expected_number_of_cards(self):
        return 4 * 4

    def page_uri(self):
        return "/gallery/royals/by/suite.html"

    def expected_cards(self):
        return royals_by_suite


class CanViewAllRoyalsByRank(GridViewSpec.CanViewAll):
    def expected_number_of_cards(self):
        return 4 * 4

    def page_uri(self):
        return "/gallery/royals/by/rank.html"

    def expected_cards(self):
        return royals_by_rank

class CanViewAllPips(GridViewSpec.CanViewAll):
    def expected_number_of_cards(self):
        return 10 * 4

    def page_uri(self):
        return "/gallery/pips/by/number.html"

    def expected_cards(self):
        pips = [
            deck.wands[0], deck.cups[0], deck.swords[0], deck.coins[0],
            deck.wands[1], deck.cups[1], deck.swords[1], deck.coins[1],
            deck.wands[2], deck.cups[2], deck.swords[2], deck.coins[2],
            deck.wands[3], deck.cups[3], deck.swords[3], deck.coins[3],
            deck.wands[4], deck.cups[4], deck.swords[4], deck.coins[4],
            deck.wands[5], deck.cups[5], deck.swords[5], deck.coins[5],
            deck.wands[6], deck.cups[6], deck.swords[6], deck.coins[6],
            deck.wands[7], deck.cups[7], deck.swords[7], deck.coins[7],
            deck.wands[8], deck.cups[8], deck.swords[8], deck.coins[8],
            deck.wands[9], deck.cups[9], deck.swords[9], deck.coins[9],
        ]
        return pips

class CanViewAllWands(GridViewSpec.CanViewAll):
    def expected_number_of_cards(self):
        return 10 + 4

    def page_uri(self):
        return "/gallery/pips/wands.html"

    def expected_cards(self):
        pips = [
            deck.wands[0], deck.wands[1], deck.wands[2], deck.wands[3], deck.wands[4],
            deck.wands[5], deck.wands[6], deck.wands[7], deck.wands[8], deck.wands[9],
            deck.wands[10], deck.wands[11], deck.wands[12], deck.wands[13]
        ]
        return pips

class CanViewAllCups(GridViewSpec.CanViewAll):
    def expected_number_of_cards(self):
        return 10 + 4

    def page_uri(self):
        return "/gallery/pips/cups.html"

    def expected_cards(self):
        return deck.cups

class CanViewAllSwords(GridViewSpec.CanViewAll):
    def expected_number_of_cards(self):
        return 10 + 4

    def page_uri(self):
        return "/gallery/pips/swords.html"

    def expected_cards(self):
        return deck.swords

class CanViewAllCoins(GridViewSpec.CanViewAll):
    def expected_number_of_cards(self):
        return 10 + 4

    def page_uri(self):
        return "/gallery/pips/coins.html"

    def expected_cards(self):
        return deck.coins

class CanViewAllTrumps(GridViewSpec.CanViewAll):
    def expected_number_of_cards(self):
        return 22

    def page_uri(self):
        return "/gallery/trumps.html"

    def expected_cards(self):
        return deck.trumps
