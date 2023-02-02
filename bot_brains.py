from aiogram import types
from loader import bot


def bot_iq(total, max_count=28):
    if 0 < total >= max_count:
        step = total % (max_count + 1)
        if step == 0:
            step = max_count
    elif 0 < total < max_count:
        step = total
    total -= step
    answer = f"Бот взял {step} конфет, осталось {total}\n"
    return answer, total
