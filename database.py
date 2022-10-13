"""
 Group 22
 Aurélien Giuglaris Michael & Antoine Dorard
 i6279204 & i6269522
"""
import sqlalchemy as sqla
from sqlalchemy.orm import sessionmaker

engine = sqla.create_engine(f"mysql+pymysql://root:z$MAEHF8N&$6tCfC@localhost/pizza_ordering_system")
conn = engine.connect()

Session = sessionmaker(bind=engine)
session = Session()