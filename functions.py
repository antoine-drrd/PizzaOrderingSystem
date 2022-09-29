from database import conn, session
from models import t_ingredient_pizzas, OrderList, Drink, Ingredient, Pizza, Desert


def query_pizza_price(pizza_id: int):
    ingredients = session.query(t_ingredient_pizzas.c.ingredient_id).filter_by(pizza_id=pizza_id).all()
    price = 0

    for ingredient_id in ingredients:
        temp = session.query(Ingredient.price).filter_by(ingredient_id=ingredient_id[0]).one()
        price = price + temp[0]

    final_price = price * 1.4
    vat = 0.09 * final_price
    return final_price + vat


def query_drink_price(drink_id: int):
    try:
        return session.query(Drink).filter_by(drink_id=drink_id).scalar().drink_price
    except:
        return 6


def query_desert_price(desert_id: int):
    try:
        return session.query(Desert).filter_by(desert_id=desert_id).scalar().drink_price
    except:
        return 6


def query_menu_drink():
    menu = {}

    drinks = [p.__dict__ for p in session.query(Drink).all()]

    for drink in drinks:
        menu.update({
            drink['drink_id']: {
                'name': drink['name'],
                'price': drink["price"]
            }
        })

    return menu


def query_menu_desert():
    menu = {}

    deserts = [d.__dict__ for d in session.query(Desert).all()]
    for desert in deserts:
        menu.update({
            desert['desert_id']: {
                'name': desert['name'],
                'price': desert["price"]
            }
        })

    return menu


def query_menu_pizza():
    menu = {}

    pizzas = [p.__dict__ for p in session.query(Pizza).all()]
    ingredient_name = {}
    ingredients = session.query(Ingredient).all()
    for i in ingredients:
        ingredient_name.update({i.__dict__.get("ingredient_id"): i.__dict__.get("name")})

    for pizza in pizzas:
        ingredient_list = session.query(t_ingredient_pizzas.c.ingredient_id).filter_by(pizza_id=pizza['pizza_id']).all()
        menu.update({
            pizza['pizza_id']: {
                'name': pizza['name'],
                'price': query_pizza_price(pizza['pizza_id']),
                'vegetarian': pizza['vegetarian'],
                'ingredients': [ingredient_name[name[0]] for name in ingredient_list]
            }
        })

    return menu

