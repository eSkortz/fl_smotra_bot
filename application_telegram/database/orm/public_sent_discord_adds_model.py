from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import func, Sequence, UniqueConstraint, ForeignKeyConstraint

from database.orm._base_class import Base
from database.orm._annotations import (
    BigintPrimaryKey,
    IntegerColumn,
    BoolColumn,
    TextColumn,
    TimestampWTColumn,
)


class SentDiscordAdds(Base):
    __tablename__ = "sent_discord_adds"
    __table_args__ = (
        UniqueConstraint("message_id", "channel_id"),
        ForeignKeyConstraint(["user_id"], ["users.id"]),
    )
    id: Mapped[BigintPrimaryKey] = mapped_column(Sequence("sent_discord_adds_id_seq"))
    user_id: Mapped[IntegerColumn] = mapped_column(nullable=False)
    message_id: Mapped[TextColumn] = mapped_column(nullable=False)
    channel_id: Mapped[TextColumn] = mapped_column(nullable=False)
    is_reaction: Mapped[BoolColumn] = mapped_column(nullable=False, default=False)
    is_deleted: Mapped[BoolColumn] = mapped_column(nullable=False, default=False)
    created_at: Mapped[TimestampWTColumn] = mapped_column(
        nullable=True, default=func.now()
    )
    updated_at: Mapped[TimestampWTColumn] = mapped_column(
        nullable=True, default=func.now(), onupdate=func.now()
    )
