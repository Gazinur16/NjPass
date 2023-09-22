import asyncio
import time
from misc import bot


# TODO Проверь это на нескольких пользователях!
async def del_msr_key(chat_id: int, mes_id: int, start_time):
    while True:
        if time.monotonic() - start_time > 60 * 3:
            await bot.delete_message(chat_id=chat_id, message_id=mes_id)
            break

        await asyncio.sleep(10)


def is_latin(msg_user: str):  # проверяем что все символы латинские
    return all(ord(c) < 128 for c in msg_user)

# async def _example1():
#     add_button(11, 'привет', 'Хелло')
#
#
# if __name__ == '__main__':
#     asyncio.run(_example1())
