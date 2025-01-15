from bs4 import BeautifulSoup
from collections import namedtuple
from django.test import TestCase

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
        self.check_wands_row(table)

    def check_wands_row(self, table):
        row = table.find("tr", {"id": "wands"})
        self.assertIsNotNone(row)

        cells = row.select("td > a")

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
        self.assertEqual(len(cells), len(uri_parts))

        for part, tag in zip(uri_parts, cells):
            url = f"https://en.wikipedia.org/wiki/Rider%E2%80%93Waite_Tarot#/media/File:{part.file}"
            self.assertEqual(url, tag['href'])

            img = tag.find("img")
            self.assertIsNotNone(img)
            img_src = f"https://upload.wikimedia.org/wikipedia/commons/{part.prefix}/{part.file}"
            self.assertEqual(img_src, img['src'])
