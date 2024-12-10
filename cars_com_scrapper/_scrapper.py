from typing import Final
import time
import requests
import io
from PIL import Image
import os

import selenium
from bs4 import BeautifulSoup
from selenium import webdriver

__all__ = ["CarsComScrapper"]


class _UrlSpecifier:
    def __init__(self, max_page_num: int, color: str, base_url: str):
        """
        Page specifiers for the mobile.de webpage

        :param max_page_num: (int) max page number to stop the iterator
        :param color: (str) string representation of the color in the url specifier
        """
        self._pgn: int = 1
        self._vhc: str = "car"
        self._pgs: Final[int] = 50
        self._color: Final[str] = color

        self._base_url = base_url
        self._max_page_num = max_page_num

    def __str__(self):
        page_str = "" if self._pgn == 1 else f"&page={self._pgn}"
        return f"{self._base_url}/?dealer_id=&exterior_color_slugs[]={self._color}&include_shippable=true&keyword=&list_price_max=&list_price_min=&makes[]=&maximum_distance=20&mileage_max=&monthly_payment={page_str}&page_size=100&sort=best_match_desc&stock_type=all&year_max=&year_min=&zip="

    def __next__(self):
        if self._pgn > self._max_page_num:
            self._pgn = 1
            raise StopIteration
        current_specifier = str(self)
        self._pgn += 1
        return current_specifier

    def __iter__(self):
        return self

    @property
    def base_url(self):
        return self._base_url


class CarsComScrapper:
    def __init__(
        self,
        pages_count: int,
        color: str,
        out_images_path: str,
        base_url: str = "https://www.cars.com/shopping/results",
        verbose: bool = False,
        test: bool = False,
    ):
        self._pages_count: int = pages_count

        self._specifier: _UrlSpecifier = _UrlSpecifier(pages_count, color, base_url)
        self._out_images_path: str = out_images_path

        self._verbose: bool = verbose
        self._test: bool = test

        self._color: str = color

        self._saved_image_index: int = 0

    @staticmethod
    def _create_driver(url: str):
        options = webdriver.EdgeOptions()
        options.add_argument("--headless")

        driver = selenium.webdriver.Edge(options=options)
        driver.implicitly_wait(3)
        driver.get(url)

        # give driver time to load the page
        time.sleep(3)
        return driver

    def _save_image_from_url(self, img_url: str):
        image_content = requests.get(img_url).content
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file).convert("RGB")

        os.makedirs(self._out_images_path, exist_ok=True)

        fpath = self._out_images_path + f"/{self._saved_image_index}.png"
        image.save(fpath, "PNG")
        self._saved_image_index += 1

    def _run_one_page(self, url: str):
        page_driver = self._create_driver(url)

        html = page_driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        image_tags = soup.find_all("img", class_="vehicle-image")
        img_alt = ""

        scrapped = 0
        for image_tag in image_tags:
            if img_alt == image_tag.attrs["alt"]:
                # skip all the other images of the same car,
                # as these can be interior images (which we don't want)
                continue
            scrapped += 1

            if self._test:
                continue

            self._save_image_from_url(image_tag.attrs["src"])
            img_alt = image_tag.attrs["alt"]

        return scrapped

    def run(self):
        scrapped_count = 0

        if self._verbose:
            print(
                f"[INFO] Scrapping data from {self._specifier.base_url}, color={self._color}"
            )

        for i, url in enumerate(self._specifier):
            if self._verbose:
                print(f"[INFO] page {i+1} out of {self._pages_count}\r", end="")

            scrapped_count += self._run_one_page(url)

        if self._verbose:
            print("\n[INFO] Scrapping finished")

        return scrapped_count
