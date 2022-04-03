from food_data import util
import re
import sys
import argparse


def get_by_brand(brand_owner):
    data = util.get_data()
    return [i for i in data if re.search(str(brand_owner), str(i["brand_owner"]), flags=re.I)]


def get_by_description(search_expression):
    data = util.get_data()
    if '*' in search_expression:
        search_expression = search_expression.replace('*', '.*')
    return [i for i in data if re.search(search_expression, i['description'], flags=re.I)]


def filter_by_category(category, data):
    return [i for i in data if i["branded_food_category"] == category]


if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args) <= 1:
        print('Usage: python -m food_data.find -b <brand> | -d <description>')

    result = None
    for i in args[::2]:
        if i is None:
            print('Invalid user input')
            break
        if i == '-b':
            result = get_by_brand(args[args.index(i) + 1])
        if i == '-d':
            result = get_by_description(args[args.index(i) + 1])
    if '-c' in args[::2]:
        result = filter_by_category(args[args.index('-c') + 1], result)
    for i in result:
        if result is not None:
            print(' '.join([str(i['fdc_id']), str(i['brand_owner']), str(i['description'])]))
