import json
from mindee import Client, PredictResponse, product


def get_api_key():
    with open('../secrets.json', 'r') as file:
        secrets = json.load(file)
    return secrets['mindeeReceipt']

def api_output(image_path):
    mindee_client = Client(get_api_key())
    input_doc = mindee_client.source_from_path(image_path)
    result: PredictResponse = mindee_client.parse(product.ReceiptV5, input_doc)
    output = result.document
    return output

def process_receipt(image_path, self=None):
    print("Processing image:", image_path)
    out = str(api_output(image_path))
    half = []
    lines = out.split("\n")

    i = 0
    while i < len(lines):
        if lines[i].startswith("  +"):
            half.append(lines[i+1])
            i += 2
        else:
            i += 1

    last_unit_price_index = None
    for i, line in enumerate(reversed(half)):
        if 'Unit Price' in line:
            last_unit_price_index = len(half) - 1 - i
            break

    if last_unit_price_index is not None:
        pass  # Process as needed

    item_names = []
    qty = []
    total_prices = []
    unit_prices = []

    broke = half[last_unit_price_index:]
    for i in range(len(broke)-1):
        curr = broke[i]
        small = curr.split('|')
        if i != 0:
            item_names.append(small[1])
            qty.append(small[2])
            total_prices.append(small[3])
            unit_prices.append(small[4])

    qty = ['1' if q.strip() == "" else q for q in qty]
    for i in range(len(unit_prices)):
        if unit_prices[i].strip() == "":
            unit_prices[i] = total_prices[i]

    item_names = [i.strip() for i in item_names]
    qty = [q.strip() for q in qty]
    total_prices = [t.strip() for t in total_prices]
    unit_prices = [u.strip() for u in unit_prices]

    for i in range(len(qty)):
        qty[i] = int(float(qty[i]))

    for i in range(len(total_prices)):
        total_prices[i] = float(total_prices[i])

    for i in range(len(unit_prices)):
        unit_prices[i] = float(unit_prices[i])

    data = [item_names, qty, total_prices, unit_prices]
    print(item_names)
    print(qty)
    print(total_prices)
    print(unit_prices)
    return data


    #db_connect = '/Users/jainamshah/PycharmProjects/Wastefree/recipe.db'

