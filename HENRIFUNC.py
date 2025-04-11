import re                      # We use regex to search for number patterns.
import os                      # This helps us work with file paths.
from bs4 import BeautifulSoup  # BeautifulSoup makes HTML parsing easy.

def extract_order(filename):
    """
    This function extracts the order details from a Deliveroo HTML receipt.
    It returns a dictionary with the order number, total paid, delivery fee, 
    and the date/time (taken from the file name).
    """
    # --- Step 1: Load and parse the HTML file ---
    with open(filename, "r", encoding="utf-8") as file:
        html_content = file.read()  # Read the entire file content.
    soup = BeautifulSoup(html_content, "html.parser")  # Create a BeautifulSoup object.

    # Initialize our variables to store the order details.
    order_number = None
    order_total_paid = None
    delivery_fee = None
    order_datetime = None  # We'll extract the datetime later from the file name.

    # --- Step 2: Extract the Order Number ---
    # We search all <h2> tags for one that contains "Commande n°".
    h2_tags = soup.find_all("h2")
    for h2 in h2_tags:
        # Get the text from the <h2> tag, join nested text with a space, and trim extra spaces.
        text = h2.get_text(separator=" ", strip=True)
        if "Commande n°" in text:
            m = re.search(r"Commande n°\s*(\d+)", text)
            if m:
                order_number = m.group(1)  # Capture the number.
                break  # We only need the first match.

    # --- Step 3: Extract Delivery Fee and Total Paid from Table Rows ---
    # We expect these values to be in a table row where one <p> contains the label 
    # and another <p> holds the amount.
    trs = soup.find_all("tr")
    for tr in trs:
        p_tags = tr.find_all("p")
        if len(p_tags) >= 2:
            label = p_tags[0].get_text(strip=True).lower()  # Get and lowercase the label.
            amount_text = p_tags[1].get_text(strip=True)      # The amount text.
            # If the label suggests it is the delivery fee...
            if "frais de livraison" in label:
                m = re.search(r"€\s*(\d+(?:[\.,]\d+)?)", amount_text)
                if m:
                    delivery_fee = m.group(1).replace(",", ".")
                
                else:
                        delivery_fee = "free"
            # If the label suggests it is the total amount...
            elif label == "total" or label.startswith("total"):
                m = re.search(r"€\s*(\d+(?:[\.,]\d+)?)", amount_text)
                if m:
                    order_total_paid = m.group(1).replace(",", ".")
    
    # --- Step 4: Extract the Date/Time from the File Name ---
    # We assume the filename is formatted like "Fri_01_Nov_2019_12_00_40_.html".
    file_name = os.path.basename(filename)      # Get just the file name.
    name_without_ext, _ = os.path.splitext(file_name)  # Remove the .html extension.
    parts = name_without_ext.split('_')          # Split by underscores.
    # We expect at least 7 parts: day-of-week, day, month, year, hour, minute, second.
    if len(parts) >= 7:
        day = parts[1]
        month = parts[2]
        year = parts[3]
        hour = parts[4]
        minute = parts[5]
        second = parts[6]
        # Build a datetime string (e.g., "2019-Nov-01 12:00:40").
        order_datetime = f"{year}-{month}-{day} {hour}:{minute}:{second}"
    else:
        order_datetime = None

    # --- Step 5: Build and return the order dictionary ---
    order = {
        "number": order_number,
        "total_paid": order_total_paid,
        "delivery_fee": delivery_fee,
        "datetime": order_datetime
    }
    return order


def extract_customer(filename):
    """
    This function extracts the customer details from the HTML receipt.
    It assumes that the information is stored in five <p> tags with the class 'alignleft'
    in the following order: name, street address, city, postcode, and phone number.
    """
    # --- Step 1: Load and parse the HTML file ---
    with open(filename, "r", encoding="utf-8") as file:
        html_content = file.read()
    soup = BeautifulSoup(html_content, "html.parser")

    # --- Step 2: Find the customer details ---
    # We search for all <p> tags that have the class "alignleft".
    customer_p_tags = soup.find_all("p", class_="alignleft")

    # Initialize variables to store customer data.
    customer_name = None
    customer_address = None
    customer_city = None
    customer_postcode = None
    customer_phone = None

    # If we have at least five matching tags, assign the values in the expected order.
    if len(customer_p_tags) >= 5:
        customer_name = customer_p_tags[0].get_text(strip=True)
        customer_address = customer_p_tags[1].get_text(strip=True)
        customer_city = customer_p_tags[2].get_text(strip=True)
        customer_postcode = customer_p_tags[3].get_text(strip=True)
        customer_phone = customer_p_tags[4].get_text(strip=True)

    # --- Step 3: Build and return the restaurant/customer dictionary ---
    customer_info = {
        "name": customer_name,
        "address": customer_address,
        "city": customer_city,
        "postcode": customer_postcode,
        "phone_number": customer_phone
    }
    return customer_info
