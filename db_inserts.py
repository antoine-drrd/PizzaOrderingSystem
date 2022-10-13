"""
 Group 22
 Aurélien Giuglaris Michael & Antoine Dorard
 i6279204 & i6269522
"""
from database import conn, session
from models import t_ingredient_pizzas, OrderList, Drink, Ingredient


def push_ingredients():
    names = [
        "Tomato",
        "Cream",
        "Mozzarella",
        "Ham",
        "Mushrooms",
        "Tuna",
        "Salami",
        "Rucola",
        "Honey",
        "Oregano",
        "Olives",
        "Artichoke",
        "Peper",
        "Bacon",
        "Roquefort",
        "Gorgonzola",
        "Goat Cheese",
        "Merguez",
        "Truffle"]

    prices = [2, 2, 2, 3, 1, 4, 3, 2, 1, 0.5, 1, 2, 1, 4, 3, 3, 3, 3, 5]

    push_drinks_deserts()

    for name, price in zip(names, prices):
        conn.execute(f"INSERT INTO ingredient (name, price) VALUES ('{name}','{price}')")


def push_drinks_deserts():
    drinks = [
    "Water Bottle",
    "San Pellegrino",
    "CocaCola",
    "Sprite"
    ]

    drinks_prices = [2,3,3,3]

    deserts = [
    "Tiramisu",
    "Panna Cotta",
    "Semi-Freddo",
    "Vassoio di fruta"
    ]

    deserts_prices = [8,9,9,10]

    for drink, drink_price in zip(drinks, drinks_prices):
        conn.execute(f"INSERT INTO drink (name, price) VALUES ('{drink}','{drink_price}')")

    for desert, desert_price in zip(deserts, deserts_prices):
        conn.execute(f"INSERT INTO desert (name, price) VALUES ('{desert}','{desert_price}')")


def push_pizza_list():
    pizzas = [
        "Margherita",
        "Reine",
        "Quattro Fromaggi",
        "Vegetarian",
        "SweetnSalty",
        "La Mama",
        "SeaFood",
        "MeatSupreme",
        "Tartuffa",
        "AllInOne" ]

    for name in pizzas:
        conn.execute(f"INSERT INTO pizza (name) VALUES ('{name}')")


def push_pizzas_link():

    dico_pizzas = {
        "margherita": {
            "id": 1,
            "ingredients": ["Tomato", "Oregano", "Mozzarella"]
        },
        "Reine": {
            "id": 2,
            "ingredients": ["Tomato", "Oregano", "Mozzarella", "Mushrooms", "Ham"]
        },
        "Quattro Fromaggi": {
            "id": 3,
            "ingredients": ["Tomato", "Mozzarella", "Roquefort", "Gorgonzola", "Goat Cheese"]
        },
        "Vegetarian": {
            "id": 4,
            "ingredients": ["Tomato", "Oregano", "Peper", "Artichoke", "Mozzarella", "Olives"]
        },
        "SweetnSalty": {
            "id": 5,
            "ingredients": ["Cream", "Honey", "Rucola", "Salami", "Mozzarella"]
        },
        "La Mama": {
            "id": 6,
            "ingredients": ["Tomato", "Mozzarella", "Merguez", "Oregano", "Olives", "Rucola"]
        },
        "SeaFood": {
            "id": 7,
            "ingredients": ["Tomato", "Oregano", "Tuna", "Salami", "Honey"]
        },
        "MeatSupreme": {
            "id": 8,
            "ingredients": ["Tomato", "Mozzarella", "Merguez", "Salami", "Ham"]
        },
        "Tartuffa": {
            "id": 9,
            "ingredients": ["Cream", "Rucola", "Truffle", "Mozzarella"]
        },
        "AllInOne": {
            "id": 10,
            "ingredients": ["Tomato", "Rucola", "Truffle", "Mozzarella", "Gorgonzola", "Roquefort", "Goat Cheese", "Ham", "Merguez", "Mushrooms", "Olives", "Peper", "Honey"]
        }
    }

    for pizza_dico in dico_pizzas.values():
        for i in pizza_dico["ingredients"]:
            ingredient_id = session.query(Ingredient.ingredient_id).filter_by(name=i).one()[0]
            conn.execute(f"""INSERT INTO ingredient_pizzas (pizza_id, ingredient_id) VALUES ('{pizza_dico.get("id")}', '{ingredient_id}')""")


def push_postal_codes():
    for code in range(1000, 2001):
        conn.execute(f"INSERT INTO postal_code (postal_code) VALUES ({code})")


def push_delivery_persons():
    for code in range(1000, 2001):
        conn.execute(f"INSERT INTO delivery_person (postal_code, status, left_at) VALUES ({code}, 'available', null)")


if __name__ == '__main__':
    # push_ingredients()
    # push_pizza_list()
    # push_drinks_deserts()
    # push_pizzas_link()
    # push_postal_codes()
    push_delivery_persons()
