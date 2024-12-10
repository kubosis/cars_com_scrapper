![Flake8 Status](https://github.com/kubosis/cars_com_scrapper/actions/workflows/quality.yml/badge.svg)
![Tests](https://github.com/kubosis/cars_com_scrapper/actions/workflows/test.yml/badge.svg)
[![codecov](https://codecov.io/gh/kubosis/cars_com_scrapper/branch/main/graph/badge.svg?token=secrets.CODECOV_TOKEN)](https://codecov.io/gh/kubosis/fspy)



# Mobile De Scrapper
Simple web scrapper for cars.com written in python


### Installation

```bash
pip install git+https://github.com/kubosis/cars_com_scrapper
```


### How to use?

```python
from cars_com_scrapper import CarsComScrapper, colors

def main():
    for color in colors:
        scrapper = CarsComScrapper(10, color, f"out/{color}.csv", f"out/{color}/",
                                   verbose=True)
        scrapper.run()

if __name__ == '__main__':
    main()


```

### Note

This scrapper is quite simple, as it only scrapes the color and the image of the car. No other features are extracted, as they
are not needed for my task. If You need more features for your data science project, consider different tool or
adjust this one to your needs.