import traceback
import json
import requests
from sqlite3 import connect
from datetime import datetime


now = datetime.now()
connection = connect("database.sqlite")
cursor = connection.cursor()
MAIN_STOCK_ID = 1

query = ("INSERT INTO product_stocks (time, product_id, variant_id, stock_id, supply) VALUES "
                               "(?, ?, ?, ?, ?)")


def main():
    for line in range(-2, -3):
        try:
            response = requests.get(
                f"https://dummy.server/products/example?id={line}"
            )
            print(f"data downloaded from server {len(response.content)}")
            # IS FILE NEEDED?
            with open("tmp.txt", "wb") as f:
                f.write(response.content)

            product = response.json

            if product["type"] != "bundle":
                print("product loaded")

                save_product(product, cursor)

            if product["type"] == "bundle":
                print("bundle loaded")

                save_bundle(product, cursor)

        except Exception:
            print(traceback.format_exc())
            print("error")
        else:
            print("ok")


def save_product(product, cursor):
    for item in product["details"]["supply"]:
        for stock in item["stock_data"]:
            # is this id stock_id is unique?
            if stock["stock_id"] == MAIN_STOCK_ID:
                product_supply = stock["quantity"]

        params = [datetime.now(), product["id"], item["variant_id"], MAIN_STOCK_ID, product_supply]
        cursor.execute(query, params)


def save_bundle(bundle, cursor):
    products = []
    for item in bundle["bundle_items"]:
        products.append(item["id"])
    print(f"products {len(products)}")

    all_products_supply = []
    for p in products:
        resp = requests.get(
            f"https://dummy.server/products/example?id={p}"
        )
        with open("tmp.txt", "wb") as f:
            f.write(resp.content)

        bundle = resp.json
        supply = 0
        for supply_item in bundle["details"]["supply"]:
            print(supply_item)
            for stock in supply_item["stock_data"]:
                if stock["stock_id"] == MAIN_STOCK_ID:
                    supply += stock["quantity"]
        all_products_supply.append(supply)
    product_supply = min(all_products_supply)

    params = [datetime.now(), bundle["id"], None, MAIN_STOCK_ID, product_supply]
    cursor.execute(query, params)





if __name__ == "__main__":
    main()
