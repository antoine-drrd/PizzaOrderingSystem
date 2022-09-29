from functions import query_menu_desert, query_menu_pizza, query_menu_drink

class Menus:
    def __init__(self):  # <-- What a supreme bullshit
        self.menu_pizzas = {}
        self.menu_drinks = {}
        self.menu_deserts = {}

    def initialize(self):
        self.menu_pizzas = query_menu_pizza()
        self.menu_drinks = query_menu_drink()
        self.menu_deserts = query_menu_desert()

    def get_menu_pizzas(self):
        return self.menu_pizzas

    def get_menu_drinks(self):
        return self.menu_drinks

    def get_menu_deserts(self):
        return self.menu_deserts


menus = Menus()
