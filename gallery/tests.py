from collections import namedtuple

from bs4 import BeautifulSoup
from django.test import TestCase

import gallery.models

UriPart = namedtuple("UriPart", ["prefix", "file"])

class GalleryIndexViewSpecs(TestCase):
    def test_that_gallery_url_exists(self):
        response = self.client.get("/gallery/")
        self.assertIs(response.status_code, 200)

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