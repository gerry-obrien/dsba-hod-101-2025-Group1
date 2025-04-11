from restaurant import parse_restaurant
import os

if __name__ == "__main__":
    toto = []
    for root, dirs, files in os.walk("deliveroo-20250411T130225Z-001"):
        for file in files:
            if file.endswith(".html"):
                file_path = os.path.join(root, file)
                restorant = parse_restaurant(file_path)
                toto.append(restorant)
            print(restorant)
