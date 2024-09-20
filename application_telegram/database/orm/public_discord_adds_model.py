from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import func, Sequence, UniqueConstraint, ForeignKeyConstraint

from database.orm._base_class import Base
from database.orm._annotations import (
    IntegerPrimaryKey,
    IntegerColumn,
    TextColumn,
    ListTextColumn,
    TimestampWTColumn,
)


class DiscordAdds(Base):
    __tablename__ = "discord_adds"
    __table_args__ = (
        UniqueConstraint("user_id", "chapter"),
        ForeignKeyConstraint(["user_id"], ["users.id"]),
    )
    id: Mapped[IntegerPrimaryKey] = mapped_column(Sequence("discord_adds_id_seq"))
    user_id: Mapped[IntegerColumn] = mapped_column(index=True, nullable=False)
    chapter: Mapped[TextColumn] = mapped_column(nullable=False)
    text: Mapped[TextColumn] = mapped_column(nullable=False, default="")
    images: Mapped[ListTextColumn] = mapped_column(nullable=False, default=[])
    timer: Mapped[IntegerColumn] = mapped_column(nullable=False, default=180)
    last_sent: Mapped[TimestampWTColumn] = mapped_column(
        nullable=True, default=func.now()
    )
    created_at: Mapped[TimestampWTColumn] = mapped_column(
        nullable=True, default=func.now()
    )
    updated_at: Mapped[TimestampWTColumn] = mapped_column(
        nullable=True, default=func.now(), onupdate=func.now()
    )
