from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import MetaData, Sequence, UniqueConstraint
from datetime import datetime, timedelta
from db.orm.annotations import (
    IntegerPrimaryKey,
    BigintPrimaryKey,
    TextColumn,
    BoolColumn,
    BigintColumn,
    TimestampWTColumn,
    IntegerColumn,
    ListTextColumn,
)


metadata_obj = MetaData(schema="public")


class Base(DeclarativeBase):
    metadata = metadata_obj


class Users(Base):
    __tablename__ = "users"
    __table_args__ = (UniqueConstraint("telegram_id"),)
    id: Mapped[IntegerPrimaryKey] = mapped_column(Sequence("users_id_seq"))
    telegram_id: Mapped[BigintColumn] = mapped_column(index=True, nullable=False)
    telegram_name: Mapped[TextColumn] = mapped_column(nullable=True)
    discord_token: Mapped[TextColumn] = mapped_column(nullable=True)
    is_have_premium: Mapped[BoolColumn] = mapped_column(nullable=False, default=False)
    created_at: Mapped[TimestampWTColumn] = mapped_column(
        nullable=False, default=datetime.utcnow()
    )
    updated_at: Mapped[TimestampWTColumn] = mapped_column(
        nullable=False, default=datetime.utcnow()
    )


class UserPointers(Base):
    __tablename__ = "users_pointers"
    __table_args__ = (UniqueConstraint("user_id"),)
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
    updated_at: Mapped[TimestampWTColumn] = mapped_column(
        nullable=False, default=datetime.utcnow()
    )


class DiscordAdds(Base):
    __tablename__ = "discord_adds"
    __table_args__ = (UniqueConstraint("user_id", "chapter"),)
    id: Mapped[IntegerPrimaryKey] = mapped_column(Sequence("discord_adds_id_seq"))
    user_id: Mapped[IntegerColumn] = mapped_column(index=True, nullable=False)
    chapter: Mapped[TextColumn] = mapped_column(nullable=False)
    text: Mapped[TextColumn] = mapped_column(nullable=False, default="")
    images: Mapped[ListTextColumn] = mapped_column(nullable=False, default=[])
    timer: Mapped[IntegerColumn] = mapped_column(nullable=False, default=120)
    updated_at: Mapped[TimestampWTColumn] = mapped_column(
        nullable=False, default=datetime.utcnow()
    )
    last_sent: Mapped[TimestampWTColumn] = mapped_column(
        nullable=False, default=datetime.utcnow() - timedelta(days=1)
    )


class SentDiscordAdds(Base):
    __tablename__ = "sent_discord_adds"
    id: Mapped[BigintPrimaryKey] = mapped_column(Sequence("sent_discord_adds_id_seq"))
    user_id: Mapped[IntegerColumn] = mapped_column(nullable=False)
    message_id: Mapped[TextColumn] = mapped_column(nullable=False)
    channel_id: Mapped[TextColumn] = mapped_column(nullable=False)
    sent_datetime: Mapped[TimestampWTColumn] = mapped_column(nullable=False, default=datetime.utcnow())
    is_reaction: Mapped[BoolColumn] = mapped_column(nullable=False, default=False)
    is_deleted: Mapped[BoolColumn] = mapped_column(nullable=False, default=False)


class RentAdds(Base):
    __tablename__ = "rent_adds"
    id: Mapped[IntegerPrimaryKey] = mapped_column(Sequence("rent_adds_id_seq"))
    user_id: Mapped[IntegerColumn] = mapped_column(index=True, nullable=False)
    number_of_gm: Mapped[IntegerColumn] = mapped_column(index=True, nullable=False)
    add_text: Mapped[TextColumn]
    contact_link: Mapped[TextColumn] = mapped_column(nullable=False)
    created_at: Mapped[TimestampWTColumn] = mapped_column(
        nullable=False, default=datetime.utcnow()
    )
    last_check: Mapped[TimestampWTColumn] = mapped_column(
        nullable=False, default=datetime.utcnow()
    )


class Notifications(Base):
    __tablename__ = "notifications"
    __table_args__ = (UniqueConstraint("user_id", "tag"),)
    id: Mapped[IntegerPrimaryKey] = mapped_column(Sequence("notifications_id_seq"))
    user_id: Mapped[IntegerColumn] = mapped_column(index=True, nullable=False)
    tag: Mapped[TextColumn] = mapped_column(nullable=False)
    created_at: Mapped[TimestampWTColumn] = mapped_column(
        nullable=False, default=datetime.utcnow()
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


class Fishing(Base):
    __tablename__ = "fishing"
    __table_args__ = (UniqueConstraint("depth"),)
    id: Mapped[IntegerPrimaryKey] = mapped_column(Sequence("fishing_id_seq"))
    depth: Mapped[IntegerColumn] = mapped_column(nullable=False)
    text: Mapped[TextColumn] = mapped_column(nullable=False)
