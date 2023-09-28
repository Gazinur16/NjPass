import asyncio
import time

from aiogram.utils.exceptions import MessageNotModified

from kb import InlineKb
from misc import bot


# TODO Проверь это на нескольких пользователях!
# TODO Проверь ошибку при ручном удалении
async def del_new_msr_key(chat_id: int, mes_id: int, start_time):
    while True:
        if time.monotonic() - start_time > 60 * 3:
            try:
                await bot.delete_message(chat_id=chat_id, message_id=mes_id)
                break
            except MessageNotModified:
                pass

        await asyncio.sleep(10)


async def del_list_pass(chat_id: int, mes_id: int, start_time):
    while True:
        if time.monotonic() - start_time > 120:
            try:
                await bot.edit_message_text(chat_id=chat_id, message_id=mes_id,
                                            text='Окно с паролями было скрыто в целях <b>безопасности</b>',
                                            reply_markup=InlineKb.continue_see_pass())
                break
            except MessageNotModified:
                pass

        await asyncio.sleep(5)

# async def _example1():
#     add_button(11, 'привет', 'Хелло')
#
#
# if __name__ == '__main__':
#     asyncio.run(_example1())
