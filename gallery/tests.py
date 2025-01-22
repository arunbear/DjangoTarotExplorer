from http import HTTPStatus

from bs4 import BeautifulSoup
from django.test import TestCase
from django.urls import reverse

import gallery.models
from gallery.models import royals


class GalleryIndexViewSpecs(TestCase):
    def test_that_gallery_url_exists(self):
        response = self.client.get(reverse('gallery:index'))
        self.assertEqual(response.status_code, HTTPStatus.OK)

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
        self.assertEqual("All", dropdown_links[0].text)
        self.assertEqual("/gallery/royals/", dropdown_links[0].get("href"))
        self.assertEqual("Pages", dropdown_links[1].text)
        self.assertEqual("/gallery/royals/pages/", dropdown_links[1].get("href"))

    def test_that_gallery_contains_table(self):
        response = self.client.get(reverse('gallery:index'))
        soup = BeautifulSoup(response.content, features="html.parser")
        table = soup.find("table", {"id": "gallery"})
        self.assertIsNotNone(table)
        self.check_table_contents(table)

    def check_table_contents(self, table):
        deck = gallery.models.deck
        self.check_row(table, "wands", deck.wands)
        self.check_row(table, "cups", deck.cups)
        self.check_row(table, "swords", deck.swords)
        self.check_row(table, "coins", deck.coins)
        self.check_row(table, "majors1", deck.majors1)
        self.check_row(table, "majors2", deck.majors2)

    def check_row(self, table, suite, cards: list[gallery.models.Card]):
        row = table.find("tr", {"id": suite})
        self.assertIsNotNone(row, f"Table contains a {suite} row")

        cells = row.select("td > a")
        self.assertEqual(len(cells), len(cards))

        for card, tag in zip(cards, cells):
            url = f"https://en.wikipedia.org/wiki/Rider%E2%80%93Waite_Tarot#/media/File:{card.file}"
            self.assertEqual(url, tag['href'])

            img = tag.find("img")
            self.assertIsNotNone(img, f"Link contains an image")
            img_src = f"https://upload.wikimedia.org/wikipedia/commons/{card.uri_key}/{card.file}"
            self.assertEqual(img_src, img['src'])

class GalleryRoyalsViewAllBySuite(TestCase):
    def test_that_all_royals_can_can_be_viewed(self):
        response = self.client.get("/gallery/royals/")
        self.assertEqual(HTTPStatus.OK, response.status_code)

        soup = BeautifulSoup(response.content, features="html.parser")
        grid = soup.find("div", {"class": "grid"})
        self.assertIsNotNone(grid)
        self.check_grid_contents(grid)

    def check_grid_contents(self, grid):
        links = grid.select("a")
        self.assertEqual(len(links), 4 * 4)
        for card, link in zip(royals.by_suite, links):
            with self.subTest():
                url = f"https://en.wikipedia.org/wiki/Rider%E2%80%93Waite_Tarot#/media/File:{card.file}"
                self.assertEqual(url, link['href'])

                img = link.find("img")
                self.assertIsNotNone(img, f"Link contains an image")
                img_src = f"https://upload.wikimedia.org/wikipedia/commons/{card.uri_key}/{card.file}"
                self.assertEqual(img_src, img['src'])
