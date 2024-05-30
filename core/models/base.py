from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr


class Base(DeclarativeBase):
    # This attribute indicates that the Base class is abstract,
    # meaning it is not intended for creating instances.
    __abstract__ = True

    # This method defines the table name in the database for this model.
    # It uses the model class name and adds an "s" at the end to form the table name.
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"

    # All models require a primary key, so we declare it in the base class.
    id: Mapped[int] = mapped_column(primary_key=True)
