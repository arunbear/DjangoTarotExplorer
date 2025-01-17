from collections import namedtuple
from itertools import dropwhile

from bs4 import BeautifulSoup
from django.test import TestCase

import gallery.models

UriPart = namedtuple("UriPart", ["prefix", "file"])

class GalleryIndexViewSpecs(TestCase):
    def test_that_gallery_url_exists(self):
        response = self.client.get("/gallery/")
        self.assertIs(response.status_code, 200)

    def test_that_nav_bar_exists(self):
        response = self.client.get("/gallery/")
        soup = BeautifulSoup(response.content, features="html.parser")
        navbar = soup.find("div", {"class": "navbar"})
        self.assertIsNotNone(navbar)

        links = navbar.select("a")
        self.assertEqual(links[0].text, "About")
        self.assertEqual(links[1].text, "Minors")
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

    def test_that_gallery_contains_table(self):
        response = self.client.get("/gallery/")
        soup = BeautifulSoup(response.content, features="html.parser")
        table = soup.find("table", {"id": "gallery"})
        self.assertIsNotNone(table)
        self.check_table_contents(table)

    def check_table_contents(self, table):
        uri_parts = gallery.models.uri_parts
        self.check_row(table, "wands", uri_parts.wands)
        self.check_row(table, "cups", uri_parts.cups)
        self.check_row(table, "swords", uri_parts.swords)
        self.check_row(table, "coins", uri_parts.coins)
        self.check_row(table, "majors1", uri_parts.majors1)
        self.check_row(table, "majors2", uri_parts.majors2)

    def check_row(self, table, suite, uri_parts):
        row = table.find("tr", {"id": suite})
        self.assertIsNotNone(row, f"Table contains a {suite} row")

        cells = row.select("td > a")
        self.assertEqual(len(cells), len(uri_parts))

        for part, tag in zip(uri_parts, cells):
            url = f"https://en.wikipedia.org/wiki/Rider%E2%80%93Waite_Tarot#/media/File:{part.file}"
            self.assertEqual(url, tag['href'])

            img = tag.find("img")
            self.assertIsNotNone(img, f"Link contains an image")
            img_src = f"https://upload.wikimedia.org/wikipedia/commons/{part.prefix}/{part.file}"
            self.assertEqual(img_src, img['src'])