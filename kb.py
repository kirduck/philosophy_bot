from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


main = InlineKeyboardMarkup().add(InlineKeyboardButton("Расскажи о себе.", callback_data="about"))\
    .add(InlineKeyboardButton("Покажи книги, которые ты написал.", callback_data="books"))\

books = InlineKeyboardMarkup().add(InlineKeyboardButton("Хочу другую книгу", callback_data="books"))\
    .add(InlineKeyboardButton("Назад", callback_data="back"))

about = InlineKeyboardMarkup().add(InlineKeyboardButton("Назад", callback_data="back"))