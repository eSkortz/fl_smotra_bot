from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import func, Sequence, UniqueConstraint, ForeignKeyConstraint

from database.orm._base_class import Base
from database.orm._annotations import (
    IntegerPrimaryKey,
    IntegerColumn,
    TextColumn,
    TimestampWTColumn,
)


class Notifications(Base):
    __tablename__ = "notifications"
    __table_args__ = (
        UniqueConstraint("user_id", "tag"),
        ForeignKeyConstraint(["user_id"], ["users.id"]),
    )
    id: Mapped[IntegerPrimaryKey] = mapped_column(Sequence("notifications_id_seq"))
    user_id: Mapped[IntegerColumn] = mapped_column(index=True, nullable=False)
    tag: Mapped[TextColumn] = mapped_column(nullable=False)
    created_at: Mapped[TimestampWTColumn] = mapped_column(
        nullable=True, default=func.now()
    )
