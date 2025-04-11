from beautifulsoup4 import BeautifulSoup

def order_items(file_name):
    """
    Function to output the order items with their quantities and prices for a given order receipt html file.
    :param file_name: the name of the html file
    :return: A dictionary with the order items in the required format
    """
    with open(file_name, "r", encoding="utf-8") as file:
        html = file.read()
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table", attrs={"role": "listitem"})
    rows = table.find_all("tr")
    quantities = []
    items = []
    prices = []
    for row in rows:
        # Find all table cells (both headers and data)
        cells = row.find_all(["td", "th"])
        for cell in cells:
            p_tags_quantities = cell.find_all("p", attrs={
                "style": "font-family:HelveticaNeue, helvetica, arial, sans-serif; font-size:15px; line-height:1.4em; color:#000001; text-align:left; font-weight:normal; text-decoration:none; Margin:0 4px 0 0; padding:0; mso-line-rule:exactly;"})
            for p in p_tags_quantities:
                quantities.append(p.get_text(strip=True))

            p_tags_items = cell.find_all("p", attrs={
                "style": "font-family:HelveticaNeue, helvetica, arial, sans-serif; font-size:15px; line-height:1.4em; color:#000001; text-align:left; font-weight:normal; text-decoration:none; Margin:0; padding:0; mso-line-rule:exactly;"})
            for p in p_tags_items:
                items.append(p.get_text(strip=True))

            p_tags_prices = cell.find_all("p", attrs={
                "style": "font-family:HelveticaNeue, helvetica, arial, sans-serif; font-size:15px; line-height:1.4em; color:#828585; text-align:right; font-weight:normal; text-decoration:none; Margin:0 0 0 8px; padding:0; mso-line-rule:exactly; white-space:nowrap;"})
            for p in p_tags_prices:
                prices.append(p.get_text(strip=True))

    cleaned_prices = []
    for price in prices:
        numeric = price.replace('\xa0€', '').replace(',', '.').strip()
        numeric = float(numeric)
        cleaned_prices.append(numeric)

    cleaned_quantities = []
    for quantity in quantities:
        quant = quantity.replace('x', '').strip()
        quant = int(quant)
        cleaned_quantities.append(quant)

    dictionary = []
    for i in range(len(items)):
        temp = {"name": items[i],
                "quantity": cleaned_quantities[i],
                "price": cleaned_prices[i]}
        dictionary.append(temp)
    return dictionary

