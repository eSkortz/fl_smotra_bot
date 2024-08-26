from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import func, Sequence, UniqueConstraint, ForeignKeyConstraint

from database.orm._base_class import Base
from database.orm._annotations import (
    IntegerPrimaryKey,
    IntegerColumn,
    BoolColumn,
    TimestampWTColumn,
)


class UsersPointers(Base):
    __tablename__ = "users_pointers"
    __table_args__ = (
        UniqueConstraint("user_id"),
        ForeignKeyConstraint(["user_id"], ["users.id"]),
    )
    id: Mapped[IntegerPrimaryKey] = mapped_column(Sequence("users_pointers_id_seq"))
    user_id: Mapped[IntegerColumn] = mapped_column(index=True, nullable=False)
    transport_pointer: Mapped[BoolColumn] = mapped_column(nullable=False, default=False)
    numbers_pointer: Mapped[BoolColumn] = mapped_column(nullable=False, default=False)
    homes_pointer: Mapped[BoolColumn] = mapped_column(nullable=False, default=False)
    business_pointer: Mapped[BoolColumn] = mapped_column(nullable=False, default=False)
    clothes_pointer: Mapped[BoolColumn] = mapped_column(nullable=False, default=False)
    weapon_pointer: Mapped[BoolColumn] = mapped_column(nullable=False, default=False)
    loot_pointer: Mapped[BoolColumn] = mapped_column(nullable=False, default=False)
    services_pointer: Mapped[BoolColumn] = mapped_column(nullable=False, default=False)
    global_pointer: Mapped[BoolColumn] = mapped_column(nullable=False, default=False)
    created_at: Mapped[TimestampWTColumn] = mapped_column(
        nullable=True, default=func.now()
    )
    updated_at: Mapped[TimestampWTColumn] = mapped_column(
        nullable=True, default=func.now(), onupdate=func.now()
    )
