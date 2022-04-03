from food_data import util
import argparse
import sys


def diff_nutrition(fdc_id1, fdc_id2, scaling=False):
    data = util.get_data()
    output = list()
    value1, value2 = [i for i in data if i['fdc_id']
                      == fdc_id1 or i['fdc_id'] == fdc_id2]
    if scaling:
        value1, value2 = scale(value1, value2, fdc_id1, fdc_id2)
    if value1['serving_size_unit'] == value2['serving_size_unit']:
        diff_serving_size = value1['serving_size'] - value2['serving_size']
        output.append(('Serving Size', diff_serving_size,
                      value1['serving_size_unit']))
    for a, b in zip(value1['nutrition'], value2['nutrition']):
        if a['name'] == b['name']:
            if a['unit_name'] == b['unit_name']:
                diff_amount = a['amount'] - b['amount']
                output.append((a['name'], diff_amount, a['unit_name']))
    return output


def scale(value1, value2, fdc_id1, fdc_id2):
    scaled_value_list = []
    scaling_value = value1 if value1['serving_size']>= value2['serving_size'] else value2
    if value1['serving_size'] == scaling_value['serving_size']:
        value2['serving_size'] = scaling_value['serving_size']
    else:
        value1['serving_size'] = scaling_value['serving_size']
    scaling_factor = max([value1['serving_size'], value2['serving_size']]
                         )//min([value1['serving_size'], value2['serving_size']])
    for i in scaling_value['nutrition']:
        scaled_value_list.append(
            {'name': i['name'], 'amount': i['amount']*scaling_factor, 'unit_name': i['unit_name']})
    if scaling_value['fdc_id'] == fdc_id1:
        value1['nutrition'] = scaled_value_list
    elif scaling_value['fic_id'] == fdc_id2:
        value2['nutrition'] = scaled_value_list
    return value1, value2


def diff_ingredients(fdc_id1, fdc_id2):
    data = util.get_data()
    value1, value2 = [set(util.parse_ingredients(i['ingredients']))
                      for i in data if i['fdc_id'] == fdc_id1 or i['fdc_id'] == fdc_id2]
    shared_ingredients = value1.intersection(value2)
    value1_but_not_value2 = value1.difference(value2)
    value2_but_not_value1 = value2.difference(value1)
    return shared_ingredients, value1_but_not_value2, value2_but_not_value1


if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args) <= 1:
        print('Usage: python -m food_data.compare -n <fdc_id_1> <fdc_id_2>')
    if all(i is not None for i in args[1:2]):
        if args[0] == '-n':
            for i in diff_nutrition(int(args[1]), int(args[2]), scaling=('-s' in args)):
                print(str(i[0]) + ': ' + str(i[1]) + ' ' + str(i[2].lower()))
        if args[0] == '-i':
            op1, op2, op3 = diff_ingredients(int(args[1]), int(args[2]))
            for i in op1:
                print('  ' + str(i))
            for i in op2:
                print('- ' + str(i))
            for i in op3:
                print('+ ' + str(i))
