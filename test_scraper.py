import unittest
from unittest.mock import patch
import os
import tempfile
import main


class Base(unittest.TestCase):
    """
    Base class for tests
    """
    pass

class TestScraper(Base):
    """
    Class for testing Scraper class
    """
    def setUp(self):
        self.scraper = main.Scraper()

    def test_constants_init(self):
        self.assertEqual(self.scraper.url, "https://vk.com/@yvkurse", "Expected url of @yvkurse group in VK to parse")
        self.assertEqual(self.scraper.csv_file, "yvkurse_articles.csv", "Expected csv file to be called yvkurse_articles.csv ")

    def test_init_session(self):
        self.assertNotEqual(self.scraper.session, None, 'Session is expected to be initialized')

    def test_scrape(self):
        self.scraper.scrape()
        self.assertNotEqual(len(self.scraper.articles), 0, "Parsed articles list should not be empty")
    
    def test_saving_csv(self):
        self.scraper.scrape() 
        self.scraper.save_csv()
        self.assertTrue(os.path.exists('yvkurse_articles.csv'), 'yvkurse_articles.csv should present')


if __name__ == '__main__':
    unittest.main()
