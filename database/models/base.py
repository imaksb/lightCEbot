from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import mapped_column 
from typing_extensions import Annotated
from sqlalchemy.ext.declarative import declared_attr

int_pk = Annotated[int, mapped_column(primary_key=True)]


class Base(DeclarativeBase):
    pass 


class TableNameMixin:
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + "s"
