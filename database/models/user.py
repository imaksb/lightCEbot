
from sqlalchemy import BIGINT, Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from database.models.base import Base, TableNameMixin 


class User(Base,  TableNameMixin):
    telegram_id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=False)
    group: Mapped[int] = mapped_column(Integer, default=1)
    get_update: Mapped[bool] = mapped_column(Boolean, default=1)
    full_name: Mapped[str] = mapped_column(String)
