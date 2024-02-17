from db.orm.schema_public import Cars, UserPointers


BOOL_TO_STATUS_ADDS = {True: "вкл ✅", False: "выкл ❌"}

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

EMOJI_BY_ADDS_CLASS = {
    "transport": "🚗",
    "numbers": "🎱",
    "homes": "🏠",
    "business": "🏦",
    "clothes": "🥋",
    "weapon": "🔫",
    "loot": "📦",
    "services": "💵",
    "global": "📊",
}

CHAPTER_CLASSIFICATION = {
    "transport": {"emoji": "🚗", "name": "Транспорт"},
    "numbers": {"emoji": "🎱", "name": "Номера"},
    "homes": {"emoji": "🏠", "name": "Дома"},
    "business": {"emoji": "🏦", "name": "Бизнесы"},
    "clothes": {"emoji": "🥋", "name": "Одежда"},
    "weapon": {"emoji": "🔫", "name": "Оружие"},
    "loot": {"emoji": "📦", "name": "Лут-предметы"},
    "services": {"emoji": "💵", "name": "Услуги"},
    "global": {"emoji": "📊", "name": "Торговая общий"},
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


def get_text_for_fishing(depth_tag: str) -> str:
    with open(f"src/fishing/{depth_tag}.txt", "r", encoding="utf-8") as file:
        content = file.read()
        return content
    

def pointer_by_chapter_name(pointers_model: UserPointers, chapter_name: str) -> str:
    match chapter_name:
        case "transport":
            return BOOL_TO_STATUS_ADDS[pointers_model.transport_pointer]
        case "numbers":
            return BOOL_TO_STATUS_ADDS[pointers_model.numbers_pointer]
        case "homes":
            return BOOL_TO_STATUS_ADDS[pointers_model.homes_pointer]
        case "business":
            return BOOL_TO_STATUS_ADDS[pointers_model.business_pointer]
        case "clothes":
            return BOOL_TO_STATUS_ADDS[pointers_model.clothes_pointer]
        case "weapon":
            return BOOL_TO_STATUS_ADDS[pointers_model.weapon_pointer]
        case "loot":
            return BOOL_TO_STATUS_ADDS[pointers_model.loot_pointer]
        case "services":
            return BOOL_TO_STATUS_ADDS[pointers_model.services_pointer]
        case "global":
            return BOOL_TO_STATUS_ADDS[pointers_model.global_pointer]
