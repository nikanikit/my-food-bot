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

BOT_TOKEN = "8992866321:AAGuEgiTJ3nQyrAwZ7XAhSOb3LVYGkWXa5o"
ADMIN_ID = 829513672

DISHES = {
    "sides": [
        {"id": "s1", "name": "Драники", "desc": "С хрустящей корочкой и сметаной. Белорусская классика.", "photo": "https://images.unsplash.com/photo-1625938145744-e38051539998?q=80&w=1000"},
        {"id": "s2", "name": "Борщ", "desc": "Наваристый, со сметаной и пампушками. Согревает душу.", "photo": "https://images.unsplash.com/photo-1547592180-85f173990554?q=80&w=1000"},
        {"id": "s3", "name": "Пюре с котлетой", "desc": "Нежное пюре и домашняя котлета. Идеальное комбо.", "photo": "https://images.unsplash.com/photo-1600891964092-4316c288032e?q=80&w=1000"},
        {"id": "s4", "name": "Жареная картошка", "desc": "Золотистая, с луком и чесночком. Опасно есть ночью.", "photo": "https://images.unsplash.com/photo-1518013431117-eb1465fa5752?q=80&w=1000"},
        {"id": "s5", "name": "Холодник", "desc": "Освежающий летний суп на кефире. То, что нужно в жару.", "photo": "https://images.unsplash.com/photo-1547592180-85f173990554?q=80&w=1000"},
    ],
    "main": [
        {"id": "m1", "name": "Пицца", "desc": "Много сыра, много начинки. Для тех, кто не хочет думать.", "photo": "https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?q=80&w=1000"},
        {"id": "m2", "name": "Русский ужин", "desc": "Сытный, традиционный. Для настоящих ценителей.", "photo": "https://images.unsplash.com/photo-1543826173-70651703c5a4?q=80&w=1000"},
        {"id": "m3", "name": "Рыба", "desc": "Запеченная или жареная. Легко, вкусно и полезно.", "photo": "https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?q=80&w=1000"},
    ],
    "salads": [
        {"id": "sl1", "name": "Салат из овощей", "desc": "Свежие овощи, зелень и ароматное масло. Витамины!", "photo": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?q=80&w=1000"},
        {"id": "sl2", "name": "Оливье", "desc": "Главный салат любого праздника. С майонезом и любовью.", "photo": "https://images.unsplash.com/photo-1600335895229-6e75511892c8?q=80&w=1000"},
        {"id": "sl3", "name": "Крабовый", "desc": "Нежный, сочный, с кукурузой. Классика жанра.", "photo": "https://images.unsplash.com/photo-1551248429-40975aa4de74?q=80&w=1000"},
        {"id": "sl4", "name": "Салат Бургер", "desc": "Все ингредиенты бургера, но в виде салата. Сыр, мясо, соус.", "photo": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?q=80&w=1000"},
    ],
    "drinks": [
        {"id": "dr1", "name": "Чай", "desc": "Черный, зеленый или с бергамотом. Уютно.", "photo": "https://images.unsplash.com/photo-1544787219-7f47ccb76574?q=80&w=1000"},
        {"id": "dr2", "name": "Квас", "desc": "Холодный, пенистый. Настоящий русский напиток.", "photo": "https://images.unsplash.com/photo-1527960471264-932f39eb5846?q=80&w=1000"},
        {"id": "dr3", "name": "Кофе", "desc": "Бодрящий эспрессо или нежный латте. Для энергии.", "photo": "https://images.unsplash.com/photo-1497935586351-b67a49e012bf?q=80&w=1000"},
        {"id": "dr4", "name": "Вода", "desc": "Просто чистая и прохладная вода. Лучший выбор для здоровья.", "photo": "https://images.unsplash.com/photo-1548839140-29a749e1cf4d?q=80&w=1000"},
        {"id": "dr5", "name": "Газировка", "desc": "Со льдом и лимоном. Праздник в стакане.", "photo": "https://images.unsplash.com/photo-1581006852262-e4307cf6283a?q=80&w=1000"},
        {"id": "dr6", "name": "Сок", "desc": "Свежевыжатый апельсиновый или яблочный.", "photo": "https://images.unsplash.com/photo-1600271886742-f049cd451bba?q=80&w=1000"},
        {"id": "dr7", "name": "Пиво", "desc": "Пенное, холодное. Отлично под рыбу или пиццу.", "photo": "https://images.unsplash.com/photo-1518176258769-f227c798150e?q=80&w=1000"},
