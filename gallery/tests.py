from abc import ABCMeta, abstractmethod
from http import HTTPStatus

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

        links = navbar.select("a")
        self.assertEqual(links[0].text, "About")
        self.assertEqual(links[1].text, "All")
        self.assertEqual(links[1].get("href"), "/gallery/")

        self.check_dropdown_for_royals(navbar)
        self.check_dropdown_for_pips(navbar)

    def check_dropdown_for_royals(self, navbar):
        dropdown = navbar.find("div", {"id": "dropdown-royals"})
        self.assertIsNotNone(dropdown)

        button = dropdown.find("button")
        self.assertRegex(button.text, "Royals")

        dropdown_content = dropdown.find("div", {"class": "dropdown-content"})
        dropdown_links = dropdown_content.select("a")
        self.assertEqual("By Suite", dropdown_links[0].text)
        self.assertEqual("/gallery/royals/by/suite", dropdown_links[0].get("href"))
        self.assertEqual("By Rank", dropdown_links[1].text)
        self.assertEqual("/gallery/royals/by/rank", dropdown_links[1].get("href"))

    def check_dropdown_for_pips(self, navbar):
        dropdown = navbar.find("div", {"id": "dropdown-pips"})
        self.assertIsNotNone(dropdown)
        button = dropdown.find("button")
        self.assertRegex(button.text, "Pips")

        dropdown_content = dropdown.find("div", {"class": "dropdown-content"})
        self.assertIsNotNone(dropdown_content)
        dropdown_links = dropdown_content.select("a")
        self.assertEqual(2, len(dropdown_links))
        self.assertEqual("By Number", dropdown_links[0].text)
        self.assertEqual("/gallery/pips/by/number", dropdown_links[0].get("href"))
        self.assertEqual("Wands", dropdown_links[1].text)
        self.assertEqual("/gallery/pips/wands", dropdown_links[1].get("href"))


class GridViewSpec:
    # Nest to prevent unittest from instantiating an ABC
    class CanViewAll(TestCase, metaclass=ABCMeta):
        def test_that_all_cards_can_can_be_viewed(self):
            response = self.client.get(self.page_uri())
            self.assertEqual(HTTPStatus.OK, response.status_code)

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
        return "/gallery/royals/by/suite/"

    def expected_cards(self):
        return royals_by_suite


class CanViewAllRoyalsByRank(GridViewSpec.CanViewAll):
    def expected_number_of_cards(self):
        return 4 * 4

    def page_uri(self):
        return "/gallery/royals/by/rank/"

    def expected_cards(self):
        return royals_by_rank

class CanViewAllPips(GridViewSpec.CanViewAll):
    def expected_number_of_cards(self):
        return 10 * 4

    def page_uri(self):
        return "/gallery/pips/by/number"

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
        return "/gallery/pips/wands/"

    def expected_cards(self):
        pips = [
            deck.wands[0], deck.wands[1], deck.wands[2], deck.wands[3], deck.wands[4],
            deck.wands[5], deck.wands[6], deck.wands[7], deck.wands[8], deck.wands[9],
            deck.wands[10], deck.wands[11], deck.wands[12], deck.wands[13]
        ]
        return pips
