from bs4 import BeautifulSoup
from django.test import TestCase

class GalleryIndexViewSpecs(TestCase):
    def test_that_gallery_url_exists(self):
        response = self.client.get("/gallery/")
        self.assertIs(response.status_code, 200)

    def test_that_gallery_contains_table(self):
        response = self.client.get("/gallery/")
        soup = BeautifulSoup(response.content, features="html.parser")
        table = soup.find("table", {"id": "gallery"})
        self.assertIsNotNone(table)
