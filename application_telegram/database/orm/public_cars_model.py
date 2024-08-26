from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import func, Sequence, UniqueConstraint

from database.orm._base_class import Base
from database.orm._annotations import (
    IntegerPrimaryKey,
    IntegerColumn,
    BoolColumn,
    TextColumn,
    TimestampWTColumn,
)


class Cars(Base):
    __tablename__ = "cars"
    __table_args__ = (UniqueConstraint("name"), UniqueConstraint("image_link"))
    id: Mapped[IntegerPrimaryKey] = mapped_column(Sequence("cars_id_seq"))
    name: Mapped[TextColumn] = mapped_column(nullable=False)
    price: Mapped[IntegerColumn] = mapped_column(nullable=False)
    classification: Mapped[TextColumn] = mapped_column(nullable=False)
    max_speed: Mapped[IntegerColumn] = mapped_column(nullable=False)
    is_body_kit: Mapped[BoolColumn] = mapped_column(nullable=False)
    trunk: Mapped[IntegerColumn] = mapped_column(nullable=False)
    tank: Mapped[IntegerColumn] = mapped_column(nullable=False)
    image_link: Mapped[TextColumn] = mapped_column(nullable=False)
    created_at: Mapped[TimestampWTColumn] = mapped_column(
        nullable=True, default=func.now()
    )
    updated_at: Mapped[TimestampWTColumn] = mapped_column(
        nullable=True, default=func.now(), onupdate=func.now()
    )
