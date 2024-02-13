from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import MetaData, Sequence
import datetime
from db.orm.annotations import (
    IntegerPrimaryKey,
    TextColumn,
    BoolColumn,
    BigintColumn,
    TimestampWTColumn,
    IntegerColumn,
    ListTextColumn
)


metadata_obj = MetaData(schema="public")


class Base(DeclarativeBase):
    metadata = metadata_obj


# class Users(Base):
#     __tablename__ = "users"
#     id: Mapped[int] = mapped_column(primary_key=True, nullable=False, unique=True)
#     name: Mapped[str] = mapped_column()


class Users(Base):
    __tablename__ = "users"
    id: Mapped[IntegerPrimaryKey] = mapped_column(Sequence('users_id_seq'))
    telegram_id: Mapped[BigintColumn] = mapped_column(index=True, nullable=False)
    telegram_name: Mapped[TextColumn] = mapped_column(nullable=True)
    discord_token: Mapped[TextColumn]
    is_have_premium: Mapped[BoolColumn] = mapped_column(nullable=False)
    created_at: Mapped[TimestampWTColumn] = mapped_column(nullable=False, default=datetime.datetime.utcnow())
    updated_at: Mapped[TimestampWTColumn] = mapped_column(nullable=False, default=datetime.datetime.utcnow())


class UserPointers(Base):
    __tablename__ = "user_pointers"
    id: Mapped[IntegerPrimaryKey] = mapped_column(Sequence('user_pointers_id_seq'))
    user_id: Mapped[IntegerColumn] = mapped_column(index=True, nullable=False)
    transport_pointer: Mapped[IntegerColumn] = mapped_column(nullable=False)
    numbers_pointer: Mapped[IntegerColumn] = mapped_column(nullable=False)
    homes_pointer: Mapped[IntegerColumn] = mapped_column(nullable=False)
    business_pointer: Mapped[IntegerColumn] = mapped_column(nullable=False)
    clothes_pointer: Mapped[IntegerColumn] = mapped_column(nullable=False)
    weapon_pointer: Mapped[IntegerColumn] = mapped_column(nullable=False)
    loot_pointer: Mapped[IntegerColumn] = mapped_column(nullable=False)
    services_pointer: Mapped[IntegerColumn] = mapped_column(nullable=False)
    global_pointer: Mapped[IntegerColumn] = mapped_column(nullable=False)


class TransportAdds(Base):
    __tablename__ = "transport_adds"
    id: Mapped[IntegerPrimaryKey] = mapped_column(Sequence('transport_adds_id_seq'))
    user_id: Mapped[IntegerColumn] = mapped_column(index=True, nullable=False)
    text: Mapped[TextColumn]
    images: Mapped[ListTextColumn]
    timer: Mapped[IntegerColumn]
    created_at: Mapped[TimestampWTColumn]
    last_sent: Mapped[TimestampWTColumn]


class NumbersAdds(Base):
    __tablename__ = "numbers_adds"
    id: Mapped[IntegerPrimaryKey] = mapped_column(Sequence('numbers_adds_id_seq'))
    user_id: Mapped[IntegerColumn] = mapped_column(index=True, nullable=False)
    text: Mapped[TextColumn]
    images: Mapped[ListTextColumn] = mapped_column(nullable=False)
    timer: Mapped[IntegerColumn] = mapped_column(nullable=False)
    created_at: Mapped[TimestampWTColumn] = mapped_column(nullable=False)
    last_sent: Mapped[TimestampWTColumn] = mapped_column(nullable=False)


class HomesAdds(Base):
    __tablename__ = "homes_adds"
    id: Mapped[IntegerPrimaryKey] = mapped_column(Sequence('homes_adds_id_seq'))
    user_id: Mapped[IntegerColumn] = mapped_column(index=True, nullable=False)
    text: Mapped[TextColumn]
    images: Mapped[ListTextColumn] = mapped_column(nullable=False)
    timer: Mapped[IntegerColumn] = mapped_column(nullable=False)
    created_at: Mapped[TimestampWTColumn] = mapped_column(nullable=False)
    last_sent: Mapped[TimestampWTColumn] = mapped_column(nullable=False)


class BusinessAdds(Base):
    __tablename__ = "business_adds"
    id: Mapped[IntegerPrimaryKey] = mapped_column(Sequence('business_adds_id_seq'))
    user_id: Mapped[IntegerColumn] = mapped_column(index=True, nullable=False)
    text: Mapped[TextColumn]
    images: Mapped[ListTextColumn] = mapped_column(nullable=False)
    timer: Mapped[IntegerColumn] = mapped_column(nullable=False)
    created_at: Mapped[TimestampWTColumn] = mapped_column(nullable=False)
    last_sent: Mapped[TimestampWTColumn] = mapped_column(nullable=False)


class ClothesAdds(Base):
    __tablename__ = "clothes_adds"
    id: Mapped[IntegerPrimaryKey] = mapped_column(Sequence('clothes_adds_id_seq'))
    user_id: Mapped[IntegerColumn] = mapped_column(index=True, nullable=False)
    text: Mapped[TextColumn]
    images: Mapped[ListTextColumn] = mapped_column(nullable=False)
    timer: Mapped[IntegerColumn] = mapped_column(nullable=False)
    created_at: Mapped[TimestampWTColumn] = mapped_column(nullable=False)
    last_sent: Mapped[TimestampWTColumn] = mapped_column(nullable=False)


class WeaponAdds(Base):
    __tablename__ = "weapon_adds"
    id: Mapped[IntegerPrimaryKey] = mapped_column(Sequence('weapon_adds_id_seq'))
    user_id: Mapped[IntegerColumn] = mapped_column(index=True, nullable=False)
    text: Mapped[TextColumn]
    images: Mapped[ListTextColumn] = mapped_column(nullable=False)
    timer: Mapped[IntegerColumn] = mapped_column(nullable=False)
    created_at: Mapped[TimestampWTColumn] = mapped_column(nullable=False)
    last_sent: Mapped[TimestampWTColumn] = mapped_column(nullable=False)


class LootAdds(Base):
    __tablename__ = "loot_adds"
    id: Mapped[IntegerPrimaryKey] = mapped_column(Sequence('loot_adds_id_seq'))
    user_id: Mapped[IntegerColumn] = mapped_column(index=True, nullable=False)
    text: Mapped[TextColumn]
    images: Mapped[ListTextColumn] = mapped_column(nullable=False)
    timer: Mapped[IntegerColumn] = mapped_column(nullable=False)
    created_at: Mapped[TimestampWTColumn] = mapped_column(nullable=False)
    last_sent: Mapped[TimestampWTColumn] = mapped_column(nullable=False)


class ServicesAdds(Base):
    __tablename__ = "services_adds"
    id: Mapped[IntegerPrimaryKey] = mapped_column(Sequence('services_adds_id_seq'))
    user_id: Mapped[IntegerColumn] = mapped_column(index=True, nullable=False)
    text: Mapped[TextColumn]
    images: Mapped[ListTextColumn] = mapped_column(nullable=False)
    timer: Mapped[IntegerColumn] = mapped_column(nullable=False)
    created_at: Mapped[TimestampWTColumn] = mapped_column(nullable=False)
    last_sent: Mapped[TimestampWTColumn] = mapped_column(nullable=False)


class GlobalAdds(Base):
    __tablename__ = "global_adds"
    id: Mapped[IntegerPrimaryKey] = mapped_column(Sequence('global_adds_id_seq'))
    user_id: Mapped[IntegerColumn] = mapped_column(index=True, nullable=False)
    text: Mapped[TextColumn]
    images: Mapped[ListTextColumn] = mapped_column(nullable=False)
    timer: Mapped[IntegerColumn] = mapped_column(nullable=False)
    created_at: Mapped[TimestampWTColumn] = mapped_column(nullable=False)
    last_sent: Mapped[TimestampWTColumn] = mapped_column(nullable=False)


class RentAdds(Base):
    __tablename__ = "rent_adds"
    id: Mapped[IntegerPrimaryKey] = mapped_column(Sequence('rent_adds_id_seq'))
    user_id: Mapped[IntegerColumn] = mapped_column(index=True, nullable=False)
    number_of_gm: Mapped[IntegerColumn] = mapped_column(index=True, nullable=False)
    add_text: Mapped[TextColumn]
    contact_link: Mapped[TextColumn] = mapped_column(nullable=False)
    created_at: Mapped[TimestampWTColumn] = mapped_column(nullable=False)
    last_check: Mapped[TimestampWTColumn] = mapped_column(nullable=False)
    is_deleted: Mapped[BoolColumn] = mapped_column(nullable=False)


class Notifications(Base):
    __tablename__ = "notifications"
    id: Mapped[IntegerPrimaryKey] = mapped_column(Sequence('notifications_id_seq'))
    user_id: Mapped[IntegerColumn] = mapped_column(index=True, nullable=False)
    tag: Mapped[TextColumn] = mapped_column(nullable=False)
    is_deleted: Mapped[BoolColumn] = mapped_column(nullable=False)


class Cars(Base):
    __tablename__ = "cars"
    id: Mapped[IntegerPrimaryKey] = mapped_column(Sequence('cars_id_seq'))
    name: Mapped[TextColumn] = mapped_column(nullable=False)
    price: Mapped[IntegerColumn] = mapped_column(nullable=False)
    classification: Mapped[TextColumn] = mapped_column(nullable=False)
    max_speed: Mapped[IntegerColumn]
    is_body_kit: Mapped[BoolColumn]
    trunk: Mapped[IntegerColumn]
    tank: Mapped[IntegerColumn]
    image_link: Mapped[TextColumn]


class CarTags(Base):
    __tablename__ = "car_tags"
    id: Mapped[IntegerPrimaryKey] = mapped_column(Sequence('car_tags_id_seq'))
    car_id: Mapped[IntegerColumn] = mapped_column(index=True, nullable=False)
    tag: Mapped[TextColumn] = mapped_column(index=True, nullable=False)


class Fishing(Base):
    __tablename__ = "fishing"
    id: Mapped[IntegerPrimaryKey] = mapped_column(Sequence('fishing_id_seq'))
    depth: Mapped[IntegerColumn]
    text: Mapped[TextColumn]


class Lootboxes(Base):
    __tablename__ = "lootboxes"
    id: Mapped[IntegerPrimaryKey] = mapped_column(Sequence('lootboxes_id_seq'))
    name: Mapped[TextColumn]
    photo: Mapped[TextColumn]
    text: Mapped[TextColumn]


class Crafts(Base):
    __tablename__ = "crafts"
    id: Mapped[IntegerPrimaryKey] = mapped_column(Sequence('crafts_id_seq'))
    name: Mapped[TextColumn]
    photo: Mapped[TextColumn]
    text: Mapped[TextColumn]