import re
import os
from bs4 import BeautifulSoup

def extract_order(filename):

    # We load and parse the HTML file
    with open(filename, "r", encoding="utf-8") as file:
        html_content = file.read()
    soup = BeautifulSoup(html_content, "html.parser")

    # We nitialize our variables to store the order details.
    order_number = None
    order_total_paid = None
    delivery_fee = None
    order_datetime = None

    # We search all <h2> tags for one that contains "Commande n°" and then we capture the number.
    h2_tags = soup.find_all("h2")
    for h2 in h2_tags:
        text = h2.get_text(separator=" ", strip=True)
        if "Commande n°" in text:
            m = re.search(r"Commande n°\s*(\d+)", text)
            if m:
                order_number = m.group(1)
                break
    # We extract Delivery Fee and Total Paid from Table Rows.
    trs = soup.find_all("tr")
    for tr in trs:
        p_tags = tr.find_all("p")
        if len(p_tags) >= 2:
            label = p_tags[0].get_text(strip=True).lower()
            amount_text = p_tags[1].get_text(strip=True)
            if "frais de livraison" in label:
                m = re.search(r"€\s*(\d+(?:[\.,]\d+)?)", amount_text)
                if m:
                    delivery_fee = m.group(1).replace(",", ".")
                else:
                        delivery_fee = "free"
            elif label == "total" or label.startswith("total"):
                m = re.search(r"€\s*(\d+(?:[\.,]\d+)?)", amount_text)
                if m:
                    order_total_paid = m.group(1).replace(",", ".")

    # We extract the date and assume the filename is formatted like "Fri_01_Nov_2019_12_00_40_.html".
    file_name = os.path.basename(filename)
    name_without_ext, _ = os.path.splitext(file_name)
    parts = name_without_ext.split('_')
    if len(parts) >= 7:
        day = parts[1]
        month = parts[2]
        year = parts[3]
        hour = parts[4]
        minute = parts[5]
        second = parts[6]
        order_datetime = f"{year}-{month}-{day} {hour}:{minute}:{second}"
    else:
        order_datetime = None

    order = {
        "number": order_number,
        "total_paid": order_total_paid,
        "delivery_fee": delivery_fee,
        "datetime": order_datetime
    }
    return order

def extract_customer(filename):
    with open(filename, "r", encoding="utf-8") as file:
        html_content = file.read()
    soup = BeautifulSoup(html_content, "html.parser")

    # We find the customer details. To do that, we search for all <p> tags that have the class "alignleft".
    customer_p_tags = soup.find_all("p", class_="alignleft")

    # We initialize variables to store customer data.
    customer_name = None
    customer_address = None
    customer_city = None
    customer_postcode = None
    customer_phone = None
    # We assign the values in the expected order. If we have at least 5 matching p tags.
    if len(customer_p_tags) >= 5:
        customer_name = customer_p_tags[0].get_text(strip=True)
        customer_address = customer_p_tags[1].get_text(strip=True)
        customer_city = customer_p_tags[2].get_text(strip=True)
        customer_postcode = customer_p_tags[3].get_text(strip=True)
        customer_phone = customer_p_tags[4].get_text(strip=True)

    customer_info = {
        "name": customer_name,
        "address": customer_address,
        "city": customer_city,
        "postcode": customer_postcode,
        "phone_number": customer_phone
    }
    return customer_info
