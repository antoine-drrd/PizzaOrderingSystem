"""
 Group 22
 Aurélien Giuglaris Michael & Antoine Dorard
 i6279204 & i6269522
"""
import random
import sys

import print_functions as pf
import functions as f
from rich.console import Console
from rich.table import Table
import menus
from database import session, conn
from models import Customer, PostalCode, OrderList, DeliveryPerson, Pizza, Drink, Desert, t_order_pizza, t_order_drink, \
    t_order_desert

from datetime import datetime
import datetime as dt

import copy

cons = Console()


def generate_discount_code(length):
    return ("{0:0"+str(length)+"x}").format(random.randrange(16**length))


def run():
    while True:
        cons.print("What do you want to do ?")
        cons.print("1 - menu")

        cons.print("2 - immediately cancel last order")
        response = input("> ")
        if response == "2":
            phone_number = input("please enter your phone number: ")
            customer = session.query(Customer).filter_by(phone_number=phone_number.strip()).scalar()
            if customer is None:
                cons.print("You are not inside our database, you've never ordered before")
            else:
                want_to_cancel = datetime.now()
                last_order = session.query(OrderList).filter_by(customer_id=customer.customer_id).all()
                if len(last_order) <= 0:
                    cons.print("You don't have any order")
                else:
                    last_order = last_order[-1]
                    ordered_at = last_order.ordered_at
                    if want_to_cancel - ordered_at >= dt.timedelta(minutes=5):
                        cons.print("You cannot cancel your order, you ordered more than 5 Minutes ago")
                    else:
                        customer.nb_ordered_pizzas -= len(conn.execute("SELECT pizza_id FROM order_pizza WHERE order_id=%s", [last_order.order_id]).all())
                        session.delete(last_order)
                        session.commit()
                        cons.print("You've successfully deleted your order, what are you going to eat now !?")

        elif response == "1":
            # Ordering management
            pf.print_menu_pizza()
            ordered_pizzas = []
            raw_input = ''
            while raw_input == '':
                cons.print("Please select the number corresponding to each pizza you want to order, separate each number with ',': ")
                raw_input = input("> ")
                ordered_pizzas = raw_input.strip().split(",")
                if raw_input == '':
                    cons.print("Please take at least one pizza")
                else:
                    break

            current_price = 0.0
            for x in ordered_pizzas:
                current_price = current_price + f.query_pizza_price(int(x))

            cons.print("You will be paying: " + str(round(current_price, 2)))
            check_out_drinks = input("Do you want to order drinks, type 'yes' to agree or anything else for 'no':")
            ordered_drinks = []
            if check_out_drinks == 'yes':
                pf.print_menu_drinks()
                cons.print("Please select the number corresponding to each drinks you want to order, separate each number with ',':")
                ordered_drinks = input("> ").split(",")
                for x in ordered_drinks:
                    current_price = current_price + f.query_drink_price(int(x))

            cons.print("You will be paying: " + str(round(current_price, 2)))
            check_out_deserts = input("Do you want to order deserts, type 'yes' to agree or anything else for 'no':")
            ordered_deserts = []
            if check_out_deserts == 'yes':
                pf.print_menu_deserts()
                cons.print("Please select the number corresponding to each desert you want to order, separate each number with ',':")
                ordered_deserts = input("> ").split(",")
                for x in ordered_deserts:
                    current_price = current_price + f.query_desert_price(int(x))

            cons.print("Thank you for your order, you will be paying: " + str(round(current_price, 2)))

            #Information management
            check_phone = input("We need to check if you are in our system please enter your phone number without spaces:")

            customer = session.query(Customer).filter_by(phone_number=check_phone.strip()).scalar()
            customer_id = 0
            if customer is None:
                cons.print("You are not registered inside our database system, please enter the following information")
                user_data = info_input(check_phone)
                customer = Customer(first_name=user_data["first_name"],
                                    last_name=user_data["last_name"],
                                    phone_number=user_data["phone_number"],
                                    street=user_data["street_name"],
                                    house_number=user_data["house_number"],
                                    city=user_data["city"],
                                    postal_code=user_data["postal_code"],
                                    nb_ordered_pizzas=0)
                # new user is pushed at the end once the order is paid
                # discount code stays null and nb_ordered_pizzas will be appended right before the push
                session.add(customer)
                session.flush()
                customer_id = customer.customer_id
                session.commit()

            else:
                customer_id = customer.customer_id

            previous_pizza_amount = customer.nb_ordered_pizzas
            cons.print("")
            if previous_pizza_amount >= 10 or customer.discount_code is not None:
                discount_code = customer.discount_code
                # Generate code if not yet in the db, but if it was, show the code again as a reminder
                if discount_code is None:
                    discount_code = generate_discount_code(20)
                    customer.discount_code = discount_code

                cons.print("You are eligible to a 10% off discount. Here is your code to apply during checkout: [bold][green]" + str(discount_code) + "[/green][/bold]")
                if previous_pizza_amount >= 10:
                    customer.nb_ordered_pizzas = previous_pizza_amount - 10

                session.commit()
            else:
                if 10 - previous_pizza_amount - len(ordered_pizzas) > 0:
                    cons.print("Once you order " + str(10 - previous_pizza_amount - len(ordered_pizzas)) + " you will receive a 10% discount on your next order")
                else:
                    cons.print(" You have ordered exactly : " + str(previous_pizza_amount + len(ordered_pizzas)) + " \n You will receive a discount code with a 10% off value for your next order")

            #Checkout management
            customer.nb_ordered_pizzas += len(ordered_pizzas)
            cons.print("")
            cons.print("Enter your promotional code press enter if don't have any")
            promo_code = input("> ")
            if len(promo_code) > 0 and promo_code == customer.discount_code:
                current_price = current_price * 0.9
                customer.discount_code = None
            session.commit()

            cons.print("The price you have to pay is :" + str(round(current_price, 2)))

            #Update DB order management
            #push client_id in order database
            new_order = OrderList(customer_id=customer_id, ordered_at=datetime.now()) #order_id is created automatically
            session.add(new_order)
            session.flush()
            order_id = new_order.order_id
            session.commit()

            #Push pizzas in order_pizza database
            for id in ordered_pizzas:
                conn.execute("INSERT INTO order_pizza (order_id, pizza_id) VALUES (%s, %s)", [order_id, id])

            if ordered_drinks != []:
                for id in ordered_drinks:
                    conn.execute("INSERT INTO order_drink (order_id, drink_id) VALUES (%s, %s)", [order_id, id])

            if ordered_deserts != []:
                for id in ordered_deserts:
                    conn.execute("INSERT INTO order_desert (order_id, desert_id) VALUES (%s, %s)", [order_id, id])

            cons.print("... Thank you for your order")
            cons.print("")

            #Delivery management
            delivery_persons = session.query(DeliveryPerson).filter_by(postal_code=customer.postal_code).all()

            counter = 0
            shortest_time = datetime.max

            delivery_person = None
            for dp in delivery_persons:
                left_at = dp.left_at

                if left_at is None or datetime.now() - left_at > dt.timedelta(minutes=30):
                    left_at = datetime.now()
                    session.query(DeliveryPerson).filter_by(delivery_person_id=dp.delivery_person_id).update({'left_at': left_at})
                    session.commit()
                    #10 Min prep + 15 Min delivery
                    cons.print("You will be delivered in around 25 minutes")
                    break
                else:
                    if left_at < shortest_time:
                        shortest_time = left_at
                        delivery_person = dp

                    counter += 1

            if counter == len(delivery_persons):
                now = datetime.now()
                time_left = now - shortest_time
                time_left_final = dt.timedelta(minutes=30) - time_left
                time_left_final = time_left_final + dt.timedelta(minutes=25)
                cons.print("Your estimated delivery time is "+str(int(time_left_final.seconds/60)) + " minutes")

            cons.print("")
            cons.print("This is the content of your order: ")

            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("Pizzas")
            table.add_column("Drinks")
            table.add_column("Deserts")

            pizza_names = []
            for x, id in enumerate(ordered_pizzas):
                pizza_names.append(session.query(Pizza).filter_by(pizza_id=id).scalar().name)

            drink_names = []
            for x, id in enumerate(ordered_drinks):
                drink_names.append(session.query(Drink).filter_by(drink_id=id).scalar().name)

            desert_names = []
            for x, id in enumerate(ordered_deserts):
                desert_names.append(session.query(Desert).filter_by(desert_id=id).scalar().name)

            rows = []
            max_size = max(len(ordered_pizzas), len(ordered_drinks), len(ordered_deserts))
            for i in range(max_size):
                curr_row = []
                if i < len(pizza_names):
                    curr_row.append(pizza_names[i])
                else:
                    curr_row.append("")

                if i < len(drink_names):
                    curr_row.append(drink_names[i])
                else:
                    curr_row.append("")

                if i < len(desert_names):
                    curr_row.append(desert_names[i])
                else:
                    curr_row.append("")

                rows.append(curr_row)

            for i in range(len(rows)):
                table.add_row(rows[i][0], rows[i][1], rows[i][2])

            cons.print(table)
            cons.print("")

            cons.print("We hope to see you again at our Pizzeria de la Mama")


def info_input(phone_number):
    stop = False
    counter = 0
    while not stop:
        if counter > 0:
            cons.print("Please enter your phone number again:")
            phone_number = input("> ")

        cons.print("Please enter your first name:")
        first_name = input("> ")
        cons.print("Please enter your last name:")
        last_name = input("> ")
        cons.print("Please enter your street name:")
        street_name = input("> ")
        while True:
            cons.print("Please enter your house number:")
            house_number = input("> ")
            try:
                int(house_number)
                break
            except ValueError:
                cons.print("Enter an integer")

        cons.print("Please enter the city in which you live:")
        city = input("> ")

        while True:
            cons.print("Please enter your postal code <= 4 chars:")
            postal_code = input("> ")
            if len(postal_code) <= 4:
                if session.query(PostalCode).filter_by(postal_code=postal_code).scalar() is not None:
                    break
                else:
                    cons.print("Your delivery address is not in our range, we cannot deliver to you")
            else:
                cons.print("Enter a postal code with less than 4 characters")


        cons.print("This is the information you entered, is everything correct? Type 'yes' to go to the next step or anything else for 'no':")
        cons.print(" [bold] Phone Number: [/bold]"+phone_number)
        cons.print(" [bold] Firstname: [/bold]"+first_name)
        cons.print(" [bold] Lastname: [/bold]"+last_name)
        cons.print(" [bold] Street: [/bold]"+street_name)
        cons.print(" [bold] House Number: [/bold]"+house_number)
        cons.print(" [bold] City: [/bold]"+city)
        cons.print(" [bold] Postal Code: [/bold]"+postal_code)
        answer = input("Your answer: ")

        if answer == 'yes':
            stop = True
            return {
                "first_name": first_name,
                "last_name": last_name,
                "street_name": street_name,
                "house_number": house_number,
                "city": city,
                "postal_code": postal_code,
                "phone_number": phone_number
                }
        else:
            counter = 1
            cons.print("Please enter your information again.", style="bold red")


if __name__ == '__main__':
    # Initializing all 3 menus (pizza, drinks, deserts)
    menus.menus.initialize()

    # Starting the loop
    run()
