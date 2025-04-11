from bs4 import BeautifulSoup
import re

def parse_restaurant(link):
    with open(file=link,mode="r",encoding="utf-8") as file:
        html_content = file.read()
    soup = BeautifulSoup(html_content, "html.parser")
    restaurant = {}
    name = soup.find('p', style="font-family:HelveticaNeue, helvetica, arial, sans-serif; font-size:15px; line-height:1.4em; color:#000001; text-align:left; font-weight:bolder; text-decoration:none; Margin:0 0 8px 0; padding:0; mso-line-rule:exactly;").text.strip()
    adress = soup.find_all('p', style="font-family:HelveticaNeue, helvetica, arial, sans-serif; font-size:15px; line-height:1.4em; color:#828585; text-align:left; font-weight:normal; text-decoration:none; Margin:0; padding:0; mso-line-rule:exactly;")
    phone_match = re.search(r'(\+33\s?[1-9](?:[\s.-]?\d{2}){4})', html_content )

    phone_number = phone_match.group(1) if phone_match else None

    restaurant["name"] = name
    restaurant["adress"] = adress[0].text.strip()
    restaurant["city"] = adress[1].text.strip()
    restaurant["postcode"] = adress[2].text.strip()
    restaurant["phone_number"] = phone_number
    resto = {"restaurant": restaurant}

    return resto
