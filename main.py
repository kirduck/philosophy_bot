import aiogram.utils.exceptions

from aiogram import types, Dispatcher, executor, Bot
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from aiogram.dispatcher.filters.state import State, StatesGroup
import asyncio
import json
import random
import time
import kb




philosophy_arr = [
    "Я считал, что жить означает исследовать абсурд, бунтовать против него. <b>Я извлекаю из абсурда три следствия — мой бунт, мою свободу и мою страсть. Посредством одной только работы ума я обращаю в правило жизни то, что было приглашением к смерти, — и отвергаю самоубийство</b>",
    "Я думаю, человек имеет выбор: либо жить в своем времени, приспосабливаясь к нему, либо пытаться возвыситься над ним, но можно и вступить с ним в сделку: <b>жить в своем веке и веровать в вечное</b>. Последнее мне не импонирует. Я считаю, что от абсурда можно заслониться погружением в вечное, спастись бегством в иллюзии повседневности или следованием какой-то идее. Иными словами, снизить давление абсурда можно с помощью мышления.",
    "Людей, пытающихся возвыситься над абсурдом, я называю завоевателями. Классические образцы людей-завоевателей я находил в произведениях французского писателя А. Мальро. Думаю, завоеватель богоподобен, <b>он знает свое рабство и не скрывает этого</b>, путь его к свободе освещает знание. <b>Завоеватель — это идеал человека, но быть таковым — это удел немногих</b>.",
    "Мне кажется, бунт — это не противоестественное состояние, а вполне закономерное. <b>Для того чтобы жить, человек должен бунтовать </b>, но делать это надо, не отвлекаясь от первоначально выдвинутых благородных целей. В опыте абсурда страдание имеет индивидуальный характер, в бунтарском же порыве оно становится коллективным. Причем <b>зло, испытанное одним человеком, становится чумой, заразившей всех</b>.",
    "Мне кажется, <b>в этом мире действует, один закон — закон силы, и вдохновляется он волей к власти</b>, которая может реализовываться с помощью насилия.",
    "Я полагаю, что для достижения счастья богатство не обязательно. Он был против достижения индивидуального счастья путем принесения несчастья другим. <b>Самая большая заслуга человека, чтобы жить в одиночестве и безвестности</b>",
    "Я считаю буржуазную свободу выдумкой. <b>Свобода — дело угнетенных, и ее традиционными защитниками всегда были выходцы из притесняемого народа</b>.",
    "Формулируя свою нравственную позицию, я писал в <b>Записных книжках</b>: <b>Мы должны служить справедливости, потому что существование наше устроено несправедливо, должны умножать взращивать счастье и радость, потому что мир наш несчастен</b>."
]
books = []
with open("json_libs/books_info.json", "r") as f:
    file_add = json.load(f)
    for i in file_add:
        books.append(i)

bot = Bot(token='5278938017:AAEgs0BuKmQlA3sgOVQk9Wpqx7IAoHsw7Wk')
dp = Dispatcher(bot, storage=MemoryStorage())

class States(StatesGroup):
    MainState = State()

@dp.message_handler(commands=["start"])
async def start(msg: types.Message, state: FSMContext):
    await state.set_state(States.MainState.state)
    await msg.delete()
    main_mess = await bot.send_message(msg.from_user.id, "<i>Подожди немного, скоро здесь появится информация о моей философии.</i>", parse_mode="HTML")
    await bot.send_message(msg.from_user.id, parse_mode="HTML",
                           text=f"<i>🖐👁👃👁\n Привет, {msg.from_user.first_name}, я <b>Альбер Камю</b>! Что тебе подсказать?</i> ",
                           reply_markup=kb.main)
    async with state.proxy() as data:
        data["id"] = msg.from_user.id
        with open("json_libs/ids.json", "r") as f:
            file_ids = json.load(f)
        with open("json_libs/ids.json", "w") as f:
            if str(data["id"]) not in file_ids:
                file_ids[data["id"]] = main_mess["message_id"]
            json.dump(file_ids, f)


@dp.callback_query_handler(text="books", state=States.MainState.state)
async def push(call: types.CallbackQuery):
    rand = random.choice(books)
    with open("json_libs/books_info.json", "r") as f:
        file_book = json.load(f)
        try:
            await call.message.edit_text(f"<b>{rand}</b>\n\n\n<a href='{file_book[rand]}'>Перейти в источник</a>", parse_mode="HTML", reply_markup=kb.books)
        except aiogram.utils.exceptions.MessageNotModified:
            pass


@dp.callback_query_handler(text="about", state=States.MainState.state)
async def about(call: types.CallbackQuery):
    await call.message.edit_text("<i>Я родился <b>7 ноября 1913</b> года в Алжире, на ферме «Сан-Поль». Мой отец, Люсьен Камю, во время Первой мировой войны был смертельно ранен. Моя мать, Кутрин Сантэ, которая по национальности была испанкой, полуглухая и неграмотная, вместе с детьми переехала в Алжир. Жили очень бедно. Мать, чтобы содержать семью, работала на фабрике, уборщицей."
                                 "\nС <b>1918</b> по <b>1923</b> годы я учился в начальной школе и закончил ее с отличием. "
                                 "\nС <b>1932</b> по <b>1937</b> годы я был студентом Алжирского университета. В <b>1937</b> году вышел мой первый сборник «Изнанка и лицо»."
                                 "\nКогда я закончил обучение в университете, возглавляя Алжирский дом культуры, мы вместе с будущей женой Франсин Фор переехали в Оран и преподавали там частные уроки. Позже переехали в Париж."
                                 "\nВ <b>1940</b> году закончил работу по пьесе «Посторонний». А в декабре меня уволили из «Пари-суар». Я вернулся в Оран, там учил детей французскому языку в школе."
                                 "\nВ <b>1942</b> году выходит «Посторонний». С <b>1943</b> года печатается в газете «Комба», позже занимаю должность редактора. В <b>1944</b> году закончен роман «Чума», его опубликовали только через <b>3</b> года."
                                 "\nВ <b>1956</b> году я написал рассказ «Падение», а через год вышел сборник «Изгнание и царство». В <b>1957</b> году получил Нобелевскую премию.</i>", parse_mode="HTML",reply_markup=kb.about)

@dp.callback_query_handler(text="back", state=States.MainState.state)
async def back(call: types.CallbackQuery):
    await call.message.edit_text(parse_mode="HTML",
                           text=f"<i>🖐👁👃👁\n Привет, {call.from_user.first_name}, я <b>Альбер Камю</b>! Что тебе подсказать?</i> ",
                           reply_markup=kb.main)


@dp.message_handler()
async def default(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        await msg.delete()
        data["mess"] = await bot.send_message(data["id"], "<i>Извини, но я не могу с тобой разговаривать.</i>", parse_mode="HTML")
        await asyncio.sleep(3)
        await bot.delete_message(chat_id=msg.from_user.id, message_id=data["mess"]["message_id"])


async def philosophy():
    while True:
        with open("json_libs/ids.json", "r") as f:
            file_ph = json.load(f)
            for li in file_ph:
                try:
                    await bot.edit_message_text(chat_id=int(li), message_id=file_ph[li], text=f"<i><b>Моя философия</b>:\n{random.choice(philosophy_arr)}</i>", parse_mode="HTML")
                except aiogram.utils.exceptions.MessageNotModified:
                    pass
        await asyncio.sleep(20)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(philosophy())
    executor.start_polling(dp, skip_updates=True)
