import os
import json
from urllib.request import urlretrieve


def download_data():
    url = 'http://faculty.cs.niu.edu/~dakoop/cs503-2022sp/a3/food-data-sample.json'
    fname = 'food-data-sample.json'
    return urlretrieve(url, os.path.join(os.path.dirname(__file__), 'food-data-sample.json'))


def get_data():
    fname = os.path.join(os.path.dirname(__file__), 'food-data-sample.json')
    return json.load(open(fname))

def parse_ingredients(ingredients):
    return [i.strip() for i in ingredients.split(',')]