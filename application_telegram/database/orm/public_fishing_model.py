from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import func, Sequence, UniqueConstraint

from database.orm._base_class import Base
from database.orm._annotations import (
    IntegerPrimaryKey,
    IntegerColumn,
    TextColumn,
    ListTextColumn,
    TimestampWTColumn,
)


class Fishing(Base):
    __tablename__ = "fishing"
    __table_args__ = (UniqueConstraint("depth"),)
    id: Mapped[IntegerPrimaryKey] = mapped_column(Sequence("fishing_id_seq"))
    depth: Mapped[IntegerColumn] = mapped_column(nullable=False)
    text: Mapped[TextColumn] = mapped_column(nullable=False)
    created_at: Mapped[TimestampWTColumn] = mapped_column(
        nullable=True, default=func.now()
    )
    updated_at: Mapped[TimestampWTColumn] = mapped_column(
        nullable=True, default=func.now(), onupdate=func.now()
    )
