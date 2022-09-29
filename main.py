import random

import print_functions as pf
import functions as f
from rich.console import Console
import menus
from database import session
from models import Customer, PostalCode

cons = Console()


def generate_discount_code(length):
    return ("{0:0"+str(length)+"x}").format(random.randrange(16**length))


def run():
    while True:
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
        if check_out_drinks == 'yes':
            pf.print_menu_drinks()
            cons.print("Please select the number corresponding to each drinks you want to order, separate each number with ',':")
            ordered_drinks = input("> ").split(",")
            for x in ordered_drinks:
                current_price = current_price + f.query_drink_price(int(x))

        cons.print("You will be paying: " + str(round(current_price, 2)))
        check_out_deserts = input("Do you want to order deserts, type 'yes' to agree or anything else for 'no':")
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
        if customer is None:
            cons.print("You are not registered inside our database system, please enter the following information")
            user_data = info_input()
            customer = Customer(first_name=user_data["first_name"],
                                last_name=user_data["last_name"],
                                phone_number=check_phone,
                                street=user_data["street_name"],
                                house_number=user_data["house_number"],
                                city=user_data["city"],
                                postal_code=user_data["postal_code"],
                                nb_ordered_pizzas=0)
            # new user is pushed at the end once the order is payed
            # discount code stays null and nb_ordered_pizzas will be appended right before the push
            session.add(customer)
            session.commit()

        previous_pizza_amount = customer.nb_ordered_pizzas

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
        cons.print("Enter your promotional code press enter if don't have any")
        promo_code = input("> ")
        if len(promo_code) > 0 and promo_code == customer.discount_code:
            current_price = current_price * 0.9
            customer.discount_code = None
        cons.print("The price you have to pay is :" + str(round(current_price, 2)))
        cons.print("... Thank you for your order")
        session.commit()

        #Delivery management


def info_input():
    stop = False
    while not stop:
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
        cons.print(" first_name: "+first_name)
        cons.print(" last_name: "+last_name)
        cons.print(" street_name: "+street_name)
        cons.print(" house_number: "+house_number)
        cons.print(" city: "+city)
        cons.print(" postal_code: "+postal_code)
        answer = input("Your answer: ")

        if answer == 'yes':
            stop = True
            return {
                "first_name": first_name,
                "last_name": last_name,
                "street_name": street_name,
                "house_number": house_number,
                "city": city,
                "postal_code": postal_code
                }
        else:
            cons.print("Please enter your information again.")


if __name__ == '__main__':
    # Initializing all 3 menus (pizza, drinks, deserts)
    menus.menus.initialize()

    # Starting the loop
    run()
