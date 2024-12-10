"""
Author: Jakub Sukdol
Github: kubosis

This is driver code file for simple webscrapper for mobile.de

The WebScrapper scrapes only picture of the car and the
"""

from cars_com_scrapper import CarsComScrapper, colors

def main():
    for color in colors:
        scrapper = CarsComScrapper(10, color, f"out/{color}.csv", f"out/{color}/",
                                   verbose=True)
        scrapper.run()

if __name__ == '__main__':
    main()
