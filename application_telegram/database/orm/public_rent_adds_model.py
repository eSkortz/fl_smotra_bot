from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import func, Sequence, UniqueConstraint, ForeignKeyConstraint

from database.orm._base_class import Base
from database.orm._annotations import (
    IntegerPrimaryKey,
    IntegerColumn,
    TextColumn,
    TimestampWTColumn,
)


class RentAdds(Base):
    __tablename__ = "rent_adds"
    __table_args__ = (ForeignKeyConstraint(["user_id"], ["users.id"]),)
    id: Mapped[IntegerPrimaryKey] = mapped_column(Sequence("rent_adds_id_seq"))
    user_id: Mapped[IntegerColumn] = mapped_column(index=True, nullable=False)
    number_of_gm: Mapped[IntegerColumn] = mapped_column(index=True, nullable=False)
    add_text: Mapped[TextColumn]
    contact_link: Mapped[TextColumn] = mapped_column(nullable=False)
    last_check: Mapped[TimestampWTColumn] = mapped_column(
        nullable=True, default=func.now()
    )
    created_at: Mapped[TimestampWTColumn] = mapped_column(
        nullable=True, default=func.now()
    )
