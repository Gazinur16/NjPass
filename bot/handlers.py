import asyncio
from aiogram import types

import kb
from kb import InlineKb, StaticKb
from blanks import Blanks
from misc import dp

"""COMMAND HANDLERS"""


@dp.message_handler(commands=['start'])
async def start_handler(m: types.Message):
    await m.answer_sticker(sticker=Blanks.hello_sticker,
                           reply_markup=StaticKb.put_user_main_menu())
    await asyncio.sleep(0.8)
    await m.answer(text=Blanks.main_menu, reply_markup=InlineKb.show_user_menu())


# @dp.message_handler(commands=['help'])
# async def help_handler(m: types.Message):
#     await m.answer('Hello')


"""MESSAGE HANDLERS"""


@dp.message_handler(text=Blanks.user_menu)
async def on_main_menu(m: types.Message):
    await m.answer(text=Blanks.main_menu, reply_markup=InlineKb.show_user_menu())


"""CALLBACK HANDLERS"""


@dp.callback_query_handler(kb.InlineKb.cd_but_main_menu.filter())
async def on_main_menu(cq: types.CallbackQuery):
    await cq.message.edit_text(
        text=Blanks.info_about_us
    )


@dp.callback_query_handler(kb.InlineKb.cd_but_about_us.filter())
async def on_about_us(
        cq: types.CallbackQuery):
    await cq.message.edit_text(
        text=Blanks.info_about_us
    )


@dp.callback_query_handler(kb.InlineKb.cd_but_our_services.filter())
async def on_our_services(
        cq: types.CallbackQuery
):
    await cq.message.edit_text(
        text=f'Наши услуги:'
    )


@dp.callback_query_handler(kb.InlineKb.cd_but_portfolio.filter())
async def on_portfolio(
        cq: types.CallbackQuery
):
    await cq.message.edit_text(
        text=f'Наше портфолио: '
    )


@dp.callback_query_handler(kb.InlineKb.cd_but_order_consultation.filter())
async def on_consultation(
        cq: types.CallbackQuery
):
    await cq.message.edit_text(
        text=f'Консультация: '
    )


@dp.callback_query_handler(kb.InlineKb.cd_but_invite_a_friend.filter())
async def on_invite_a_friend(
        cq: types.CallbackQuery
):
    await cq.message.edit_text(
        text=f'Консультация: '
    )
