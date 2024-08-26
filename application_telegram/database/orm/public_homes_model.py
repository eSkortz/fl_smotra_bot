from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import func, Sequence, UniqueConstraint, ForeignKeyConstraint

from database.orm._base_class import Base
from database.orm._annotations import (
    IntegerPrimaryKey,
    IntegerColumn,
    TextColumn,
    TimestampWTColumn,
)


class Homes(Base):
    __tablename__ = "homes"
    __table_args__ = (
        UniqueConstraint("user_id", "name"),
        ForeignKeyConstraint(["user_id"], ["users.id"]),
    )
    id: Mapped[IntegerPrimaryKey] = mapped_column(Sequence("homes_id_seq"))
    user_id: Mapped[IntegerColumn] = mapped_column(index=True, nullable=False)
    name: Mapped[TextColumn] = mapped_column(nullable=False)
    expenses: Mapped[IntegerColumn] = mapped_column(nullable=True)
    balance: Mapped[IntegerColumn] = mapped_column(nullable=False)
    created_at: Mapped[TimestampWTColumn] = mapped_column(
        nullable=True, default=func.now()
    )
    updated_at: Mapped[TimestampWTColumn] = mapped_column(
        nullable=True, default=func.now(), onupdate=func.now()
    )
