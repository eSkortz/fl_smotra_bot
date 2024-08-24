from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile
from aiogram.enums.parse_mode import ParseMode

from keyboards import start_k, premium_k, support_k
from keyboards.fishing import fishing_main_k
from keyboards.discord import discord_main_k
from keyboards.cars import cars_main_k
from keyboards.rent import rent_main_k
from keyboards.property import property_main_k

from utils.func_utils import auto_registration


router = Router()


@router.message(Command("start"))
async def start_command(message: Message) -> None:
    await auto_registration(message)
    markup_inline = start_k.get()
    photo = FSInputFile("src/main.png")
    await message.answer_photo(
        photo=photo,
        caption=(
            "> 🎮 Это *SmotraAssistant*, сервис созданный для помощи при вопросах, возникающих"
            "в ходе игрового процесса на сервере SmotraRage\. *Здесь вы сможете:*\n"
            ">> ├ найти информацию об автомобилях и рыбалке\n"
            ">> ├ автоматизировать процесс торговли в [discord](https://discord.gg/smotra)\n"
            ">> ├ сдать в аренду или найти гаражные места\n"
            ">> └ настроить уведомления о пополнении домов или выполнении заданий на бизнесах"
        ),
        reply_markup=markup_inline,
        parse_mode=ParseMode.MARKDOWN_V2,
    )


@router.message(Command("premium"))
async def premium_command(message: Message) -> None:
    await auto_registration(message)
    markup_inline = premium_k.get()
    photo = FSInputFile("src/premium.png")
    await message.answer_photo(
        photo=photo,
        caption=(
            "> 💎 Это раздел покупки премиум привелегии\.\n\n"
            "> *Стоимость: 1000р навсегда\.*\n\n"
            "> Привелегия дает доступ к таймеру 60 минут \(в стандартной версии минимальная частота, "
            "с которой вы можете отправлять объявления, составляет 3 часа\)\. Помимо этого "
            "вы также получите доступ к 'премиум'\-функциям, которые будут добавлены "
            "в будущем\. Я открыт для ваших предложений, если у вас есть таковые \- можете "
            "написать их мне в личку\."
        ),
        reply_markup=markup_inline,
        parse_mode=ParseMode.MARKDOWN_V2,
    )


@router.message(Command("support"))
async def support_command(message: Message) -> None:
    await auto_registration(message)
    markup_inline = support_k.get()
    photo = FSInputFile("src/support.png")
    await message.answer_photo(
        photo=photo,
        caption=(
            "> 💭 Это раздел поддержки, если вы хотите написать какое\-либо предложение "
            "или у вас есть вопросы по работе бота \- можете описать их в чате, кликнув по кнопке ниже "
            "или написать их мне в [личку](https://t.me/eskortz_work)"
        ),
        reply_markup=markup_inline,
        parse_mode=ParseMode.MARKDOWN_V2,
    )


@router.message(Command("fishing"))
async def fishing_command(message: Message) -> None:
    await auto_registration(message)
    markup_inline = fishing_main_k.get()
    photo = FSInputFile("src/fishing.png")
    await message.answer_photo(
        photo=photo,
        caption=(
            "🐟 Это раздел рыбалки, здесь вы можете посмотреть какую рыбу на какой глубине, "
            + "на какую наживку/удочку, вы можете поймать, сколько это займет времени, и "
            + "сколько будет стоить пойманная вами рыба."
        ),
        reply_markup=markup_inline,
    )


@router.message(Command("discord"))
async def discord_command(message: Message) -> None:
    await auto_registration(message)
    markup_inline = discord_main_k.get()
    photo = FSInputFile("src/discord.png")
    await message.answer_photo(
        photo=photo,
        caption=(
            "🌐 Это раздел торговой площадки discord, в нем вы можете добавить свои "
            + "обьявления, а также добавить уведомления по ключевым словам."
        ),
        reply_markup=markup_inline,
    )


@router.message(Command("cars"))
async def cars_command(message: Message) -> None:
    await auto_registration(message)
    markup_inline = cars_main_k.get()
    photo = FSInputFile("src/cars.png")
    await message.answer_photo(
        photo=photo,
        caption=(
            "🚗 Здесь представлены категории автомобилей на сервере. В разделе 'эксклюзивы' "
            + "вы можете найти информацию об эксклюзивных транспортных средствах с кейсов или боевых пропусков."
        ),
        reply_markup=markup_inline,
    )


@router.message(Command("rent"))
async def rent_command(message: Message) -> None:
    await auto_registration(message)
    markup_inline = rent_main_k.get()
    photo = FSInputFile("src/rent.png")
    await message.answer_photo(
        photo=photo,
        caption=(
            "🏘 Это раздел аренды гм, здесь вы можете найти гм в аренду по вашим требованиям или "
            + "выставить свои гм для аренды и оставить ссылку для связи с вами. При выставлении "
            + "гм в аренду просьба указывать в описании стоимость комиссии и аренды, "
            + "чтобы арендатор понимал в какую цену ему выйдет аренда гаражных мест."
        ),
        reply_markup=markup_inline,
    )


@router.message(Command("property"))
async def rent_command(message: Message) -> None:
    await auto_registration(message)
    markup_inline = property_main_k.get()
    photo = FSInputFile("src/rent.png")
    await message.answer_photo(
        photo=photo,
        caption="""
        🏖 Это раздел вашего имущества, в данном разделе вы можете указать дома и бизнесы, которыми владеете, чтобы получать автоматические уведомления о необходимости пополнения или выполнения заданий. 
        (система не до конца автоматизированна и вам придется указать баланс и аппетит вашего дома или кол-во заданий на бизнесе, чтобы получать уведомления).
        Для удобства пользования в случае с домом будет доступна кнопка "💰 Пополнил дом до максимального баланса", а в случае с бизнесом кнопка "✅ Выполнил все задания".
        """,
        reply_markup=markup_inline,
    )
