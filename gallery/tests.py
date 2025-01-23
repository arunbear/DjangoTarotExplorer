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

        self.check_dropdown(navbar)

    def check_dropdown(self, navbar):
        dropdown = navbar.find("div", {"class": "dropdown"})
        self.assertIsNotNone(dropdown)

        button = dropdown.find("button")
        self.assertRegex(button.text, "Royals")

        dropdown_content = dropdown.find("div", {"class": "dropdown-content"})
        dropdown_links = dropdown_content.select("a")
        self.assertEqual("By Suite", dropdown_links[0].text)
        self.assertEqual("/gallery/royals/by/suite", dropdown_links[0].get("href"))
        self.assertEqual("By Rank", dropdown_links[1].text)
        self.assertEqual("/gallery/royals/by/rank", dropdown_links[1].get("href"))

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
