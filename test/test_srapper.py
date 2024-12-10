"""
Author: Jakub Sukdol
Github: kubosis

Basic tests
"""

from cars_com_scrapper import CarsComScrapper

import unittest

class TestScrapper(unittest.TestCase):
    def test_scrapper(self):
        scrapper = CarsComScrapper(1, "white", "", test=True, verbose=True)
        scrapper.run()

        assert scrapper.test_result


if __name__ == '__main__':
    unittest.main()
