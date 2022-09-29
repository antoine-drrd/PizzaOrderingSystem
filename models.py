from sqlalchemy import Column, Integer, String, Text, Table, ForeignKey, Boolean
from sqlalchemy.dialects.mysql import TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()
metadata = Base.metadata


class Desert(Base):
    __tablename__ = 'desert'

    desert_id = Column(Integer, primary_key=True)
    name = Column(String(50))
    price = Column(Integer, nullable=False)

    orders = relationship('OrderList', secondary='order_desert')


class Drink(Base):
    __tablename__ = 'drink'

    drink_id = Column(Integer, primary_key=True)
    name = Column(String(50))
    price = Column(Integer, nullable=False)

    orders = relationship('OrderList', secondary='order_drink')


class Ingredient(Base):
    __tablename__ = 'ingredient'

    ingredient_id = Column(Integer, primary_key=True)
    name = Column(String(50))
    price = Column(Integer, nullable=False)

    pizzas = relationship('Pizza', secondary='ingredient_pizzas')


class Pizza(Base):
    __tablename__ = 'pizza'

    pizza_id = Column(Integer, primary_key=True)
    name = Column(String(50))
    vegetarian = Column(Boolean, nullable=False)


class PostalCode(Base):
    __tablename__ = 'postal_code'

    postal_code = Column(String(4), primary_key=True)


class Customer(Base):
    __tablename__ = 'customer'

    customer_id = Column(Integer, primary_key=True)
    first_name = Column(String(256))
    last_name = Column(String(256))
    phone_number = Column(String(50))
    street = Column(String(100))
    house_number = Column(Integer)
    city = Column(String(100))
    postal_code = Column(ForeignKey('postal_code.postal_code'), index=True)
    nb_ordered_pizzas = Column(Integer)
    discount_code = Column(String(20))

    postal_code1 = relationship('PostalCode')


class DeliveryPerson(Base):
    __tablename__ = 'delivery_person'

    delivery_person_id = Column(Integer, primary_key=True)
    postal_code = Column(ForeignKey('postal_code.postal_code'), index=True)
    status = Column(String(20))
    left_at = Column(TIMESTAMP)

    postal_code1 = relationship('PostalCode')


t_ingredient_pizzas = Table(
    'ingredient_pizzas', metadata,
    Column('pizza_id', ForeignKey('pizza.pizza_id'), nullable=False, index=True),
    Column('ingredient_id', ForeignKey('ingredient.ingredient_id'), nullable=False, index=True)
)


class OrderList(Base):
    __tablename__ = 'order_list'

    order_id = Column(Integer, primary_key=True)
    customer_id = Column(ForeignKey('customer.customer_id'), index=True)

    customer = relationship('Customer')
    pizzas = relationship('Pizza', secondary='order_pizza')


t_order_desert = Table(
    'order_desert', metadata,
    Column('order_id', ForeignKey('order_list.order_id'), index=True),
    Column('desert_id', ForeignKey('desert.desert_id'), index=True)
)


t_order_drink = Table(
    'order_drink', metadata,
    Column('order_id', ForeignKey('order_list.order_id'), index=True),
    Column('drink_id', ForeignKey('drink.drink_id'), index=True)
)


t_order_pizza = Table(
    'order_pizza', metadata,
    Column('order_id', ForeignKey('order_list.order_id'), index=True),
    Column('pizza_id', ForeignKey('pizza.pizza_id'), index=True)
)