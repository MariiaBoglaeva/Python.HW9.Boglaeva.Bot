import random
from bot_brains import bot_iq
from aiogram import types
from loader import dp

total = 150
new_game = False
name = 'бот'
max_count = 28


def set_up():
    global new_game
    global total
    global name
    new_game = False
    total = 150
    name = 'бот'


@dp.message_handler(commands=['start'])  # как только поймает сообщения со словом start, будет выполняться
async def mess_start(message: types.Message):
    await message.answer(f'{message.from_user.first_name}, привет!\n '
                         f'Я бот для игры в конфеты, вот что я могу:\n'
                         f'/rules - показать правила игры,\n'
                         f'/set - установить исходные параметры игры\n'
                         f'/game - запуск игры\n'
                         f'/exit - досрочный выход из игры\n'
                         f'Выбери нужную команду\n')


@dp.message_handler(commands=['rules'])  # как только поймает сообщения со словом start, будет выполняться
async def mess_rules(message: types.Message):
    await message.answer(f'На столе лежит заданное количество конфет\n '
                         '(по умолчанию - 150)\n '
                         'Мы будем ходить с тобой по очереди. \n'
                         'Первый ход определяется жеребьёвкой.\n'
                         'За один ход можно забрать не более 28 конфет.\n'
                         'Выигрывает тот,кто забирает последние конфеты.\n'
                         '/set *число*- для изменения стартового количества \n'
                         '/game - для начала игры \n')


@dp.message_handler(commands=['help'])  # важен порядок handlerov здесь. проверяет сверху вниз
async def mess_help(message: types.Message):
    await message.answer('Ничем не могу помочь')


@dp.message_handler(commands=['set'])
async def mess_set(message: types.Message):
    global total
    global new_game
    if not new_game:
        if message.text.split()[1].isdigit():
            if int(message.text.split()[1]) > 0:
                total = int(message.text.split()[1])
                await message.answer(f'Cтартовое кол-во конфет {total}\n /game - для запуска игры')
            else:
                await message.answer(f'Задайте число больше 0!')
        else:
            await message.answer(f'Пишите цифрами')
    else:
        await message.answer(f'Игра уже идет. Нельзя изменить параметры!')


@dp.message_handler(commands=['game'])
async def mess_game(message: types.Message):
    global new_game
    global total
    global name
    global max_count
    if new_game:
        await message.answer(f'Игра уже идет.\nДля завершения игры /exit')
    else:
        new_game = True
        lottery_num = random.randint(1, 2)
        if lottery_num == 1:
            name = message.from_user.first_name
        await message.answer(f'Игра началась\n'
                             f'Стартовое кол-во конфет: {total}\n'
                             f'Первым ходит {name}')
        if name == "бот":
            msg, res = bot_iq(total)
            total = res
            await dp.bot.send_message(message.from_user.id, msg)
            if total <= 0:
                await message.answer(f"{name} выиграл")
                new_game = False
                total = 150
                name = 'бот'
            else:
                await dp.bot.send_message(message.from_user.id, "Твой ход!")
        else:
            await dp.bot.send_message(message.from_user.id, f"{name} сколько берешь конфет?")


@dp.message_handler(commands=['exit'])
async def mess_exit(message: types.Message):
    global new_game
    if new_game:
        await message.answer(f"Игра досрочно завершена.\n "
                             f"/start - для вызова меню")
        set_up()
    else:
        await message.answer(f"Игра не была начата")


@dp.message_handler()  # если убрать из скобок Commands, то будет на прочие сообщения так отвечать
async def mess_help(message: types.Message):
    global total
    global new_game
    global name
    global max_count
    if new_game and message.text.isdigit():
        step = int(message.text)
        name = message.from_user.first_name
        if step <= max_count and step <= total:
            total -= step
            await dp.bot.send_message(message.from_user.id, f"{name} взял {step} конфет, осталось {total}")
            if total <= 0:
                await message.answer(f"{name} выиграл")
                set_up()
            else:
                name = 'бот'
                msg, res = bot_iq(total)
                total = res
                await dp.bot.send_message(message.from_user.id, msg)
                if total <= 0:
                    await message.answer(f"Бот выиграл")
                    set_up()
                else:
                    await dp.bot.send_message(message.from_user.id, "Твой ход!")
        elif step > max_count and total > max_count:
            await message.answer(f"За ход можно взять не более {max_count} конфет!")
        else:
            await message.answer(f"Можно взять не более {total} конфет!")
    else:
        await message.answer(f"Некорректный запрос\n Для вызова меню - /start")
