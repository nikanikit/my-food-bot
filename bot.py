import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, html, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

# --- НАСТРОЙКИ ---
BOT_TOKEN = "8992866321:AAGuEgiTJ3nQyrAwZ7XAhSOb3LVYGkWXa5o"
ADMIN_ID = 829513672  # Ваш ID вставлен сюда

# --- МЕНЮ (Классическое ресторанное) ---
DISHES = {
    "breakfast": [
        {"id": "b1", "name": "Сырники со сгущенкой", "desc": "Классика, которая никогда не подводит. Включает режим «заботливая»", "photo": "https://images.unsplash.com/photo-1567620905732-2d1ec7ab7445?q=80&w=1000"},
        {"id": "b2", "name": "Омлет с томатами и сыром", "desc": "Быстро, сытно и очень фотогенично.", "photo": "https://images.unsplash.com/photo-1510693206972-df098062cb71?q=80&w=1000"},
        {"id": "b3", "name": "Авокадо-тост с яйцом пашот", "desc": "Для тех утр, когда хочется почувствовать себя в дорогом ресторане.", "photo": "https://images.unsplash.com/photo-1525351484163-7529414344d8?q=80&w=1000"},
        {"id": "b4", "name": "Каша с карамелизированным бананом", "desc": "Овсянка, но не скучная, а как в лучших кофейнях.", "photo": "https://images.unsplash.com/photo-1517673132405-a56a62b18caf?q=80&w=1000"},
    ],
    "lunch": [
        {"id": "l1", "name": "Куриный суп с домашней лапшой", "desc": "Согревает душу и лечит любые печали.", "photo": "https://images.unsplash.com/photo-1547592180-85f173990554?q=80&w=1000"},
        {"id": "l2", "name": "Паста Карбонара", "desc": "Секретное оружие. Если выбрал это — ты знаешь толк в жизни.", "photo": "https://images.unsplash.com/photo-1612874742237-6526221588e3?q=80&w=1000"},
        {"id": "l3", "name": "Плов с говядиной", "desc": "Настоящий мужской обед. Много мяса, много вкуса.", "photo": "https://images.unsplash.com/photo-1543826173-70651703c5a4?q=80&w=1000"},
        {"id": "l4", "name": "Салат «Цезарь» с креветками", "desc": "Для тех, кто следит за фигурой, но не готов отказываться от вкусного.", "photo": "https://images.unsplash.com/photo-1550304943-4f24f54ddde9?q=80&w=1000"},
    ],
    "dinner": [
        {"id": "d1", "name": "Стейк с овощами гриль", "desc": "Беспроигрышный вариант для вечера.", "photo": "https://images.unsplash.com/photo-1600891964092-4316c288032e?q=80&w=1000"},
        {"id": "d2", "name": "Запеченная курица с картофелем", "desc": "Уютный ужин, после которого хочется обнять и уснуть.", "photo": "https://images.unsplash.com/photo-1598515214211-89d3c73ae83b?q=80&w=1000"},
        {"id": "d3", "name": "Дорадо в духовке с лимоном", "desc": "Немного необычно, но невероятно вкусно и легко.", "photo": "https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?q=80&w=1000"},
        {"id": "d4", "name": "Бургеры домашние", "desc": "Если хочется вредной, но безумно вкусной еды.", "photo": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?q=80&w=1000"},
    ],
    "dessert": [
        {"id": "s1", "name": "Шоколадный фондан", "desc": "Жидкий центр. Нужны ли комментарии?", "photo": "https://images.unsplash.com/photo-1606313564200-e75d5e30476c?q=80&w=1000"},
        {"id": "s2", "name": "Панна котта с ягодным соусом", "desc": "Легкий итальянский десерт.", "photo": "https://images.unsplash.com/photo-1488477181946-6428a0291777?q=80&w=1000"},
        {"id": "s3", "name": "Штрудель с яблоком и корицей", "desc": "Пахнет праздником.", "photo": "https://images.unsplash.com/photo-1568571780765-9c9b8d8b0f1b?q=80&w=1000"},
    ]
}

dp = Dispatcher()

# --- КЛАВИАТУРЫ ---
def get_main_menu():
    builder = InlineKeyboardBuilder()
    builder.button(text="🌅 Завтрак", callback_data="cat_breakfast")
    builder.button(text="☀️ Обед", callback_data="cat_lunch")
    builder.button(text="🌙 Ужин", callback_data="cat_dinner")
    builder.button(text="🍰 Десерт", callback_data="cat_dessert")
    builder.adjust(2)
    return builder.as_markup()

def get_dishes_menu(category):
    builder = InlineKeyboardBuilder()
    for dish in DISHES[category]:
        builder.button(text=dish['name'], callback_data=f"dish_{dish['id']}")
    builder.button(text="⬅️ Назад", callback_data="back_to_main")
    builder.adjust(1)
    return builder.as_markup()

# --- ХЕНДЛЕРЫ ---
@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    text = (
        f"Привет, {html.bold('сладкий')}! 👋\n\n"
        "Добро пожаловать в твое персональное меню.\n"
        "Выбери, чего бы тебе хотелось сегодня, а я передам заказ на кухню. 😉"
    )
    await message.answer(text, reply_markup=get_main_menu())

@dp.callback_query(F.data.startswith("cat_"))
async def show_category(callback: CallbackQuery):
    category = callback.data.split("_")[1]
    titles = {
        "breakfast": "🌅 Выбирай завтрак, родной:",
        "lunch": "☀️ Что на обед, хозяин?",
        "dinner": "🌙 Выбирай ужин:",
        "dessert": "🍰 Десерт для сладкого:"
    }
    await callback.message.edit_text(text=titles[category], reply_markup=get_dishes_menu(category))
    await callback.answer()

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
        await callback.message.edit_text(
            text=f"Отличный выбор! 🥂\n\n{selected_dish['name']}\n\nЯ уже передал заказ. Жди!",
            reply_markup=None
        )
        await callback.answer("Заказ принят!")
        
        admin_text = (
            f"🔔 {html.bold('Новый заказ!')}\n\n"
            f"Твой любимый выбрал:\n"
            f"🍽 {html.bold(selected_dish['name'])}\n"
            f"📝 {selected_dish['desc']}\n\n"
            f"Время готовить магию! ✨"
        )
        try:
            await callback.bot.send_message(chat_id=ADMIN_ID, text=admin_text)
        except Exception as e:
            print(f"Ошибка отправки админу: {e} (Проверьте ADMIN_ID)")

@dp.callback_query(F.data == "back_to_main")
async def back_to_main(callback: CallbackQuery):
    await callback.message.edit_text(
        text="Чего пожелает мой Хозяин сегодня?",
        reply_markup=get_main_menu()
    )
    await callback.answer()

# --- ЗАПУСК ---
async def main() -> None:
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())