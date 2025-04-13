from restaurant import parse_restaurant
from HENRIFUNC import extract_customer, extract_order
from order_items import order_items
import os
import json

### Iteration over every file contained in our folder, here named "deliveroo" but might data or anything else

if __name__ == "__main__":
    toto = []
    for root, dirs, files in os.walk("deliveroo"):
        for file in files:
            if file.endswith(".html"):
                #### Create the full path to each document
                file_path = os.path.join(root, file)
                ### iterate on each file using our functions coded separately
                restaurant = parse_restaurant(file_path)
                customer = extract_customer(file_path)
                order = extract_order(file_path)
                oi = order_items(file_path)
                ## Create a full dictionnary for each of our orders
                order_dict = {
                    "order": order,
                    "restaurant": restaurant,
                    "customer": customer,
                    "order_items": oi
                }

                ### Add every dictionnary to a list of dictionnary

                toto.append(order_dict)

                print(toto)

        with open("all_orders.json", "w", encoding="utf-8") as json_file:
                json.dump(toto, json_file, indent=4, ensure_ascii=False)
