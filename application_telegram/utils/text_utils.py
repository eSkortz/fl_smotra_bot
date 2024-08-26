from database.orm.public_cars_model import Cars
from database.orm.public_users_pointers_model import UsersPointers


BOOL_TO_STATUS_ADDS = {True: "✅ вкл", False: "❌ выкл"}

CARS_CLASSIFICATION = {
    "audi": {
        "emoji": "➰",
        "name": "Audi",
    },
    "bmw": {
        "emoji": "🌍",
        "name": "BMW",
    },
    "mercedes": {
        "emoji": "🧭",
        "name": "Mercedes",
    },
    "multi": {
        "emoji": "🌐",
        "name": "Мультибрендовые",
    },
    "lada": {
        "emoji": "🛸",
        "name": "АвтоВАЗ",
    },
    "japan": {
        "emoji": "🎌",
        "name": "Японские",
    },
    "moto": {
        "emoji": "🏍",
        "name": "Мотоциклы",
    },
    "helicopter": {
        "emoji": "🚁",
        "name": "Вертолеты",
    },
    "elite": {
        "emoji": "👑",
        "name": "Элитные",
    },
    "exclusive": {
        "emoji": "💎",
        "name": "Эксклюзивы",
    },
    "trucks": {
        "emoji": "🚛",
        "name": "Грузовики",
    },
}

CHAPTER_CLASSIFICATION = {
    "transport": {
        "emoji": "🚗",
        "name": "Транспорт",
        "channel_id": "750716702224023573",
        "pointer_column_name": "transport_pointer",
        "pointer_model": UsersPointers.transport_pointer,
    },
    "numbers": {
        "emoji": "🎱",
        "name": "Номера",
        "channel_id": "750716755336233061",
        "pointer_column_name": "numbers_pointer",
        "pointer_model": UsersPointers.numbers_pointer,
    },
    "homes": {
        "emoji": "🏠",
        "name": "Дома",
        "channel_id": "750716815080161440",
        "pointer_column_name": "homes_pointer",
        "pointer_model": UsersPointers.homes_pointer,
    },
    "business": {
        "emoji": "🏦",
        "name": "Бизнесы",
        "channel_id": "750716866837741608",
        "pointer_column_name": "business_pointer",
        "pointer_model": UsersPointers.business_pointer,
    },
    "clothes": {
        "emoji": "🥋",
        "name": "Одежда",
        "channel_id": "774748875315347477",
        "pointer_column_name": "clothes_pointer",
        "pointer_model": UsersPointers.clothes_pointer,
    },
    "weapon": {
        "emoji": "🔫",
        "name": "Оружие",
        "channel_id": "774749257177628682",
        "pointer_column_name": "weapon_pointer",
        "pointer_model": UsersPointers.weapon_pointer,
    },
    "loot": {
        "emoji": "📦",
        "name": "Лут-предметы",
        "channel_id": "1059930592743018597",
        "pointer_column_name": "loot_pointer",
        "pointer_model": UsersPointers.loot_pointer,
    },
    "services": {
        "emoji": "💵",
        "name": "Услуги",
        "channel_id": "1109229581354934412",
        "pointer_column_name": "services_pointer",
        "pointer_model": UsersPointers.services_pointer,
    },
    "global": {
        "emoji": "📊",
        "name": "Торговая общий",
        "channel_id": "750715538686083103",
        "pointer_column_name": "global_pointer",
        "pointer_model": UsersPointers.global_pointer,
    },
}


def batch_price_generator(price_str: str) -> str:
    try:
        price = int(price_str)
    except ValueError:
        return "Ivalid price parameter"
    formatted_price = "{:,}".format(price).replace(",", ".")
    return formatted_price


def generate_car_info_text(car_model: Cars) -> str:
    caption = (
        f"{CARS_CLASSIFICATION[car_model.classification]['emoji']} {car_model.name}\n\n"
        + f"🚀 Максимальная скорость: {car_model.max_speed} км/ч\n"
        + f"💰 Гос. стоимость: {batch_price_generator(car_model.price)} руб.\n"
        + f"🗿 Стоимость слива: {batch_price_generator(car_model.price * 0.75)} руб.\n"
        + f"📦 Багажник: {car_model.trunk} мест(-a)\n"
        + f"⛽️ Объем бака: {car_model.tank} л (квт/ч)\n"
        + f"🪄 Наличие обвесов: {'✅' if car_model.is_body_kit == True else '❌'}\n\n"
    )
    if car_model.classification == "helicopter":
        return caption
    caption = caption + (
        f"🛠 Тюнинг:\n"
        + f"💣 Фт с внешкой - {batch_price_generator(car_model.price * 0.22125)} руб.\n"
        + f"🧨 Фт без турбины и внешки"
        + f" - {batch_price_generator(car_model.price * 0.141)} руб.\n\n"
        + f"🔨 Двигатель - {batch_price_generator(car_model.price * 0.063)} руб.\n"
        + f"⚒ Коробка передач - {batch_price_generator(car_model.price * 0.042)} руб.\n"
        + f"🛠 Тормоза - {batch_price_generator(car_model.price * 0.036)} руб.\n"
        + f"⛏ Турбина - {batch_price_generator(car_model.price * 0.0345)} руб.\n\n"
        + f"😎 Тонировка - {batch_price_generator(car_model.price * 0.012)} руб.\n"
    )
    if (
        car_model.classification == "moto"
        or car_model.name == "Kawasaki Ninja H2R"
        or car_model.name == "BRP Can-Am Maverick"
    ):
        return caption
    caption = caption + (
        f"🔦 Ксенон/Неон - {batch_price_generator(car_model.price * 0.018)} руб.\n"
        + f"🛞 Пулестойкие покрышки - {batch_price_generator(car_model.price * 0.033)} руб.\n"
        + f"🛞 Параметры колес/высота подвески"
        + f" - {batch_price_generator(car_model.price * 0.01)} руб.\n"
    )
    return caption
