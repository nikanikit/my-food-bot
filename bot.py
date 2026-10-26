import asyncio
import logging
import sys
import os
from aiohttp import web

from aiogram import Bot, Dispatcher, html, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

BOT_TOKEN = "8992866321:AAGm-BHuABHCzWxISt39zBwbVfqDeAIOBpY"
ADMIN_ID = 829513672

DISHES = {
    "breakfast": [
        {"id": "b1", "name": "Сырники со сгущенкой", "desc": "Классика, которая никогда не подводит.", "photo": "https://images.unsplash.com/photo-1567620905732-2d1ec7ab7445?q=80&w=1000"},
        {"id": "b2", "name": "Омлет с томатами и сыром", "desc": "Быстро, сытно и очень фотогенично.", "photo": "https://images.unsplash.com/photo-1510693206972-df098062cb71?q=80&w=1000"},
        {"id": "b3", "name": "Авокадо-тост с яйцом пашот", "desc": "Для тех утр, когда хочется почувствовать себя в дорогом ресторане.", "photo": "https://images.unsplash.com/photo-1525351484163-7529414344d8?q=80&w=1000"},
        {"id": "b4", "name": "Каша с карамелизированным бананом", "desc": "Овсянка, но не скучная.", "photo": "https://images.unsplash.com/photo-1517673132405-a56a62b18caf?q=80&w=1000"},
    ],
    "lunch": [
        {"id": "l1", "name": "Куриный суп с домашней лапшой", "desc": "Согревает душу.", "photo": "https://images.unsplash.com/photo-1547592180-85f173990554?q=80&w=1000"},
        {"id": "l2", "name": "Паста Карбонара", "desc": "Секретное оружие.", "photo": "https://images.unsplash.com/photo-1612874742237-6526221588e3?q=80&w=1000"},
        {"id": "l3", "name": "Плов с говядиной", "desc": "Настоящий мужской обед.", "photo": "https://images.unsplash.com/photo-1543826173-70651703c5a4?q=80&w=1000"},
        {"id": "l4", "name": "Салат «Цезарь» с креветками", "desc": "Для тех, кто следит за фигурой.", "photo": "https://images.unsplash.com/photo-1550304943-4f24f54ddde9?q=80&w=1000"},
        {"id": "l5", "name": "Борщ", "desc": "Наваристый, со сметаной и пампушками.", "photo": "https://images.unsplash.com/photo-1547592180-85f173990554?q=80&w=1000"},
        {"id": "l6", "name": "Холодник", "desc": "Освежающий летний суп на кефире.", "photo": "https://images.unsplash.com/photo-1547592180-85f173990554?q=80&w=1000"},
    ],
    "dinner": [
        {"id": "d1", "name": "Стейк с овощами гриль", "desc": "Беспроигрышный вариант.", "photo": "https://images.unsplash.com/photo-1600891964092-4316c288032e?q=80&w=1000"},
        {"id": "d2", "name": "Запеченная курица с картофелем", "desc": "Уютный ужин.", "photo": "https://images.unsplash.com/photo-1598515214211-89d3c73ae83b?q=80&w=1000"},
        {"id": "d3", "name": "Дорадо в духовке с лимоном", "desc": "Невероятно вкусно и легко.", "photo": "https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?q=80&w=1000"},
        {"id": "d4", "name": "Бургеры домашние", "desc": "Если хочется вредной еды.", "photo": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?q=80&w=1000"},
        {"id": "d5", "name": "Пицца", "desc": "Много сыра, много начинки.", "photo": "https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?q=80&w=1000"},
        {"id": "d6", "name": "Русский ужин", "desc": "Сытный, традиционный.", "photo": "https://images.unsplash.com/photo-1543826173-70651703c5a4?q=80&w=1000"},
        {"id": "d7", "name": "Рыба", "desc": "Запеченная или жареная.", "photo": "https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?q=80&w=1000"},
        {"id": "d8", "name": "Пюре с котлетой", "desc": "Нежное пюре и домашняя котлета.", "photo": "https://images.unsplash.com/photo-1600891964092-4316c288032e?q=80&w=1000"},
        {"id": "d9", "name": "Драники", "desc": "С хрустящей корочкой и сметаной.", "photo": "https://images.unsplash.com/photo-1625938145744-e38051539998?q=80&w=1000"},
        {"id": "d10", "name": "Жареная картошка", "desc": "Золотистая, с луком и чесночком.", "photo": "https://images.unsplash.com/photo-1518013431117-eb1465fa5752?q=80&w=1000"},
    ],
    "salads": [
        {"id": "sl1", "name": "Салат из овощей", "desc": "Свежие овощи, зелень и ароматное масло.", "photo": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?q=80&w=1000"},
        {"id": "sl2", "name": "Оливье", "desc": "Главный салат любого праздника.", "photo": "https://images.unsplash.com/photo-1600335895229-6e75511892c8?q=80&w=1000"},
        {"id": "sl3", "name": "Крабовый", "desc": "Нежный, сочный, с кукурузой.", "photo": "https://images.unsplash.com/photo-1551248429-40975aa4de74?q=80&w=1000"},
        {"id": "sl4", "name": "Салат Бургер", "desc": "Все ингредиенты бургера в виде салата.", "photo": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?q=80&w=1000"},
        {"id": "sl5", "name": "Цезарь с креветками", "desc": "Классика ресторанов.", "photo": "https://images.unsplash.com/photo-1550304943-4f24f54ddde9?q=80&w=1000"},
    ],
    "drinks": [
        {"id": "dr1", "name": "Чай", "desc": "Черный, зеленый или с бергамотом.", "photo": "https://images.unsplash.com/photo-1544787219-7f47ccb76574?q=80&w=1000"},
        {"id": "dr2", "name": "Квас", "desc": "Холодный, пенистый. Настоящий русский напиток.", "photo": "https://images.unsplash.com/photo-1527960471264-932f39eb5846?q=80&w=1000"},
        {"id": "dr3", "name": "Кофе", "desc": "Бодрящий эспрессо или нежный латте.", "photo": "https://images.unsplash.com/photo-1497935586351-b67a49e012bf?q=80&w=1000"},
        {"id": "dr4", "name": "Вода", "desc": "Просто чистая и прохладная вода.", "photo": "https://images.unsplash.com/photo-1548839140-29a749e1cf4d?q=80&w=1000"},
        {"id": "dr5", "name": "Газировка", "desc": "Со льдом и лимоном.", "photo": "https://images.unsplash.com/photo-1581006852262-e4307cf6283a?q=80&w=1000"},
        {"id": "dr6", "name": "Сок", "desc": "Свежевыжатый апельсиновый или яблочный.", "photo": "https://images.unsplash.com/photo-1600271886742-f049cd451bba?q=80&w=1000"},
        {"id": "dr7", "name": "Пиво", "desc": "Пенное, холодное. Отлично под рыбу.", "photo": "https://images.unsplash.com/photo-1518176258769-f227c798150e?q=80&w=1000"},
        {"id": "dr8", "name": "Виски", "desc": "Со льдом или колой.", "photo": "https://images.unsplash.com/photo-1527281400683-1aae777175f8?q=80&w=1000"},
    ],
    "dessert": [
        {"id": "s1", "name": "Шоколадный фондан", "desc": "Жидкий центр. Нужны ли комментарии?", "photo": "https://images.unsplash.com/photo-1606313564200-e75d5e30476c?q=80&w=1000"},
        {"id": "s2", "name": "Панна котта с ягодным соусом", "desc": "Легкий итальянский десерт.", "photo": "https://images.unsplash.com/photo-1488477181946-6428a0291777?q=80&w=1000"},
        {"id": "s3", "name": "Штрудель с яблоком и корицей", "desc": "Пахнет праздником.", "photo": "https://images.unsplash.com/photo-1568571780765-9c9b8d8b0f1b?q=80&w=1000"},
        {"id": "s4", "name": "Медовик", "desc": "Тот самый, пропитанный.", "photo": "https://images.unsplash.com/photo-1568571780765-9c9b8d8b0f1b?q=80&w=1000"},
    ]
}

dp = Dispatcher()

async def handle(request):
    return web.Response(text="Bot is running!")

async def start_web_server():
    app = web.Application()
    app.router.add_get('/', handle)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get('PORT', 10000))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()

def get_main_menu():
    builder = InlineKeyboardBuilder()
    builder.button(text="🌅 Завтрак", callback_data="cat_breakfast")
    builder.button(text="☀️ Обед", callback_data="cat_lunch")
    builder.button(text="🌙 Ужин", callback_data="cat_dinner")
    builder.button(text="🥗 Салаты", callback_data="cat_salads")
    builder.button(text="🍹 Напитки", callback_data="cat_drinks")
    builder.button(text="🍰 Десерты", callback_data="cat_dessert")
    builder.adjust(2)
    return builder.as_markup()

def get_dishes_menu(category):
    builder = InlineKeyboardBuilder()
    for dish in DISHES[category]:
        builder.button(text=dish['name'], callback_data=f"dish_{dish['id']}")
    builder.button(text="⬅️ Назад в главное меню", callback_data="back_to_main")
    builder.adjust(1)
    return builder.as_markup()

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    text = f"Привет, {html.bold('сладкий')}! 👋\n\nВыбери, чего бы тебе хотелось сегодня, а я передам заказ на кухню. 😉"
    await message.answer(text, reply_markup=get_main_menu())

@dp.callback_query(F.data.startswith("cat_"))
async def show_category(callback: CallbackQuery):
    try:
        category = callback.data.split("_")[1]
        titles = {
            "breakfast": "🌅 Выбирай завтрак, родной:",
            "lunch": "☀️ Что на обед, хозяин?",
            "dinner": "🌙 Выбирай ужин:",
            "salads": "🥗 Выбирай салатик:",
            "drinks": "🍹 Что будешь пить?",
            "dessert": "🍰 Десерт для сладкого:"
        }
        # Отправляем новое сообщение
        await callback.message.answer(text=titles[category], reply_markup=get_dishes_menu(category))
        await callback.answer()
    except Exception as e:
        logging.error(f"Ошибка при выборе категории: {e}")
        await callback.answer("Произошла ошибка, попробуйте еще раз.")

@dp.callback_query(F.data.startswith("dish_"))
async def dish_selected(callback: CallbackQuery):
    dish_id = callback.data.split("_")[1]
    selected_dish = None
    for cat in DISHES.values():
        for dish in cat:
            if dish['id'] == dish_id:
                selected_dish = dish
                break
    
    if selected_dish:
        await callback.message.answer_photo(
            photo=selected_dish['photo'],
            caption=f"Отличный выбор! 🥂\n\n{html.bold(selected_dish['name'])}\n\nЯ уже передал заказ. Жди!"
        )
        await callback.answer("Заказ принят!")
        
        admin_text = f"🔔 {html.bold('Новый заказ!')}\n\nТвой любимый выбрал:\n🍽 {html.bold(selected_dish['name'])}\n📝 {selected_dish['desc']}\n\nВремя готовить магию! ✨"
        try:
            await callback.bot.send_message(chat_id=ADMIN_ID, text=admin_text)
            await callback.bot.send_photo(chat_id=ADMIN_ID, photo=selected_dish['photo'], caption=f"Заказано: {selected_dish['name']}")
        except Exception as e:
            logging.error(f"Ошибка отправки админу: {e}")

@dp.callback_query(F.data == "back_to_main")
async def back_to_main(callback: CallbackQuery):
    await callback.message.answer(text="Чего пожелает мой Хозяин сегодня?", reply_markup=get_main_menu())
    await callback.answer()

async def main() -> None:
    asyncio.create_task(start_web_server())
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
    
