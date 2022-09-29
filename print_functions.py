import math
import os

import functions as f
from rich.console import Console
from rich.table import Table
from menus import menus

cons = Console()

restaurant_name = \
    """
#######################################
#        [bold]Pizzeria De La Mama[/bold]          #
#######################################
"""

big_sep = "########################################"
medium_sep = "============================"
small_sep = "--------"


def clear_screen():
    os.system("cls")
    # cons.print("\n" * 20)


def print_title():
    cons.print(restaurant_name, style="yellow")


def print_menu_pizza():
    menu = menus.get_menu_pizzas()


    print_title()

    # Subtitle
    cons.print("Menu", style="yellow")
    cons.print(medium_sep)
    id_string = ""
    for id, pizza in menu.items():
        id_string = str(id)
        if id < 10:
            id_string = " "+str(id)
        if pizza.get("vegetarian"):
            cons.print(id_string + " ▬ [#ff3c3c]"+pizza.get("name")+"[/#ff3c3c] [bold][green]V[/green][/bold]   [green]"+str(round(pizza.get("price"), 2))+"[/green]")
        else:
            cons.print(id_string + " ▬ [#ff3c3c]"+pizza.get("name")+"[/#ff3c3c]   [green]"+str(round(pizza.get("price"), 2))+"[/green]")

        cons.print(", ".join(pizza.get("ingredients")))
        print()


def print_menu_drinks():
    menu = menus.get_menu_drinks()
    cons.print(medium_sep)

    for drink in menu.values():
        cons.print("[#28d5ff]"+drink.get("name")+"[/#28d5ff]   [green]"+str(round(drink.get("price"), 2))+"[/green]")
        print()


def print_menu_deserts():
    menu = menus.get_menu_deserts()
    cons.print(medium_sep)

    for desert in menu.values():
        cons.print("[#e0a900]"+desert.get("name")+"[/#e0a900]   [green]"+str(round(desert.get("price"), 2))+"[/green]")
        print()
