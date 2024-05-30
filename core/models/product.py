from .base import Base
from sqlalchemy.orm import Mapped


class Product(Base):
    # __tablename__ = "products"

    # Define a column 'name' in the 'products' table with data type 'str'
    name: Mapped[str]
    description: Mapped[str]
    price: Mapped[int]
