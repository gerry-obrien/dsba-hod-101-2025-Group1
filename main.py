from restaurant import parse_restaurant
from HENRIFUNC import extract_customer, extract_order
from order_items import order_items
import os
import json

if __name__ == "__main__":
    toto = []
    for root, dirs, files in os.walk("deliveroo"):
        for file in files:
            if file.endswith(".html"):
                file_path = os.path.join(root, file)
                restaurant = parse_restaurant(file_path)
                customer = extract_customer(file_path)
                order = extract_order(file_path)
                oi = order_items(file_path)

                order_dict = {
                    "order": order,
                    "customer": customer,
                    "restaurant": restaurant,
                    "order_items": oi
                }

                toto.append(order_dict)

                print(toto)

        with open("all_orders.json", "w", encoding="utf-8") as json_file:
                json.dump(toto, json_file, indent=4, ensure_ascii=False)
