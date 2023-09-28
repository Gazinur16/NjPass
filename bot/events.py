import logging
from aiogram.types import BotCommand
from misc import bot

log = logging.getLogger()


async def on_startup(*args, **kwargs):

    command_list = [
        BotCommand(command="/start", description="🚀 Запуск"),
        BotCommand(command="/reset", description="🔄 Сбросить бота"),
        BotCommand(command="/help", description="🆘 Помощь"),
        BotCommand(command="/about", description="❔ Подробнее о боте")
    ]
    await bot.set_my_commands(commands=command_list)
    log.info('Bot start')


async def on_shutdown(*args, **kwargs):
    log.info('Bot off')
