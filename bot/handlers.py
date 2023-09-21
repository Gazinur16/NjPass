import asyncio
import time
from typing import Any
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import CantParseEntities
from cryptography.fernet import Fernet
from password_generator import PasswordGenerator

import kb
from bot import db
from bot.services import del_msr_key
from bot.state import CreatePass, SavePass
from kb import InlineKb, StaticKb

from blanks import Blanks
from misc import dp, db, bot

"""COMMAND HANDLERS"""


# # Шифрование
# data = "Биба".encode()
# cipher_text = cipher_suite.encrypt(data)
# print("Шифрованный текст: ", cipher_text)
#
# # Дешифрование
# plain_text = cipher_suite.decrypt(cipher_text)
# print("Расшифрованный текст: ", plain_text.decode())


@dp.message_handler(commands=['start'])
async def start_handler(m: types.Message, state: FSMContext):
    if db.user_exists(m.from_user.id) is False:
        await m.answer(text=Blanks.hello_new_user,
                       reply_markup=InlineKb.create_msr_key())
    else:
        await m.answer(text=Blanks.hello_old_user,
                       reply_markup=StaticKb.put_user_main_menu())

    await state.finish()


# @dp.message_handler(commands=['help'])
# async def help_handler(m: types.Message):
#     await m.answer('Hello')


"""MESSAGE HANDLERS"""


# @dp.message_handler(text=Blanks.my_pass)
# async def on_my_pass(m: types.Message):
#     await m.answer(text=Blanks.input_my_msr_pass)
#
#     await MyPass.input_msr_key.set()


@dp.message_handler(text=Blanks.create_pass)
async def on_create_pass(m: types.Message, state: FSMContext):
    start_len_pass = 12

    await CreatePass.create_pass.set()
    await state.update_data(len_pass=start_len_pass)

    pwo = PasswordGenerator()
    pwo.minlen = start_len_pass
    pwo.maxlen = start_len_pass
    password = pwo.generate()

    try:
        msg_for_user = Blanks.get_create_pass(password=password,
                                              len_pass=start_len_pass)

        await m.answer(text=msg_for_user,
                       reply_markup=InlineKb.generation_control(password=password,
                                                                choose_len_pass=start_len_pass))
    except CantParseEntities:

        pwo = PasswordGenerator()
        pwo.minlen = start_len_pass
        pwo.maxlen = start_len_pass
        password = pwo.generate()

        msg_for_user = Blanks.get_create_pass(password=password,
                                              len_pass=start_len_pass)

        await m.answer(text=msg_for_user,
                       reply_markup=InlineKb.generation_control(password=password,
                                                                choose_len_pass=start_len_pass))


@dp.message_handler(text=Blanks.save_pass)
async def on_save_pass(m: types.Message):
    await m.answer(text=Blanks.input_name_pass)

    await SavePass.input_name_pass.set()


@dp.message_handler(state=SavePass.input_name_pass)
async def save_name_pass(m: types.Message, state: FSMContext):
    if len(m.text) < 20:
        await state.update_data(name_pass=m.text)

        mes_login = await m.answer(text=Blanks.input_login,
                                   reply_markup=InlineKb.skip_login())
        await state.update_data(mes_login=mes_login)

        await SavePass.next()
    else:
        await m.answer(text=Blanks.big_len_name_pass)


@dp.message_handler(state=SavePass.input_login)
async def save_login(m: types.Message, state: FSMContext):
    data = await state.get_data()
    mes_login = data.get("mes_login")

    await bot.edit_message_reply_markup(chat_id=mes_login.chat.id,  # удаляем инлайн кнопку у предыдущего сообщения
                                        message_id=mes_login.message_id,
                                        reply_markup=None)

    await state.update_data(login=m.text)
    await m.answer(text=Blanks.choose_gen_pass_or_my_pass,
                   reply_markup=InlineKb.choose_gen_pass_or_my_pass())

    await SavePass.next()


# @dp.message_handler(state=SavePass.input_pass)
# async def save_pass(m: types.Message, state: FSMContext):
#     await state.update_data(password=m.text)
#     await m.answer(text=Blanks.)
#
#     await SavePass.next()


"""CALLBACK HANDLERS"""


@dp.callback_query_handler(kb.InlineKb.cd_but_skip_login.filter(), state=SavePass.input_login)
async def on_skip_login(cq: types.CallbackQuery, state: FSMContext):
    await state.update_data(login=None)

    await cq.message.edit_text(text=Blanks.choose_gen_pass_or_my_pass,
                               reply_markup=InlineKb.choose_gen_pass_or_my_pass())

    await SavePass.next()


@dp.callback_query_handler(kb.InlineKb.cd_but_create_pass_or_mine_pass.filter(), state=SavePass.choose_pass)
async def on_choose_option_pass(cq: types.CallbackQuery, state: FSMContext, callback_data: dict[str, Any]):
    option = str(callback_data['ans'])

    if option == 'create':
        start_len_pass = 12

        await state.update_data(len_pass=start_len_pass)

        pwo = PasswordGenerator()
        pwo.minlen = start_len_pass
        pwo.maxlen = start_len_pass
        password = pwo.generate()

        await cq.message.edit_text(text=Blanks.get_create_pass(password=password, len_pass=start_len_pass),
                                   reply_markup=InlineKb.generation_control_for_save_pass(
                                       choose_len_pass=start_len_pass))


@dp.callback_query_handler(kb.InlineKb.cd_but_create_msr_key.filter())
async def on_create_msr_key(cq: types.CallbackQuery):
    if db.user_exists(cq.from_user.id) is False:

        db.add_user(tg_id=cq.from_user.id)

        key = Fernet.generate_key()  # создание Мастер-Ключа

        await cq.message.edit_text(
            text=Blanks.get_create_msr_key(key),
            reply_markup=InlineKb.send_the_key(key)
        )

        # небольшой воркер
        start_time = time.monotonic()
        asyncio.create_task(del_msr_key(cq.message.chat.id, cq.message.message_id, start_time))

    else:
        await cq.message.edit_text(
            text=Blanks.no_save_msr_key,
            reply_markup=None
        )


@dp.callback_query_handler(kb.InlineKb.cd_but_close.filter(), state="*")
async def on_close_win(cq: types.CallbackQuery, state: FSMContext):
    await cq.message.edit_text(
        text=Blanks.closet,
        reply_markup=None
    )

    await state.finish()


@dp.callback_query_handler(kb.InlineKb.cd_but_update_pass.filter(),
                           state=[CreatePass.create_pass, SavePass.choose_pass])
async def on_create_pass(cq: types.CallbackQuery, state: FSMContext):
    current_state = await state.get_state()

    if current_state == 'CreatePass:create_pass':

        data = await state.get_data()
        len_pass = data.get('len_pass')

        pwo = PasswordGenerator()
        pwo.minlen = len_pass
        pwo.maxlen = len_pass
        password = pwo.generate()

        try:
            msg_for_user = Blanks.get_create_pass(password=password,
                                                  len_pass=len_pass)

            await cq.message.edit_text(text=msg_for_user,
                                       reply_markup=InlineKb.generation_control(password=password,
                                                                                choose_len_pass=len_pass))

        except CantParseEntities:

            pwo = PasswordGenerator()
            pwo.minlen = len_pass
            pwo.maxlen = len_pass
            password = pwo.generate()

            msg_for_user = Blanks.get_create_pass(password=password,
                                                  len_pass=len_pass)

            await cq.message.edit_text(text=msg_for_user,
                                       reply_markup=InlineKb.generation_control(password=password,
                                                                                choose_len_pass=len_pass))

    else:

        data = await state.get_data()
        len_pass = data.get('len_pass')

        pwo = PasswordGenerator()
        pwo.minlen = len_pass
        pwo.maxlen = len_pass
        password = pwo.generate()

        try:

            msg_for_user = Blanks.get_create_pass(password=password,
                                                  len_pass=len_pass)

            await cq.message.edit_text(text=msg_for_user,
                                       reply_markup=InlineKb.generation_control_for_save_pass(choose_len_pass=len_pass))

        except CantParseEntities:

            data = await state.get_data()
            len_pass = data.get('len_pass')

            pwo = PasswordGenerator()
            pwo.minlen = len_pass
            pwo.maxlen = len_pass
            password = pwo.generate()

            msg_for_user = Blanks.get_create_pass(password=password,
                                                  len_pass=len_pass)

            await cq.message.edit_text(text=msg_for_user,
                                       reply_markup=InlineKb.generation_control_for_save_pass(choose_len_pass=len_pass))


@dp.callback_query_handler(kb.InlineKb.cd_but_len_pass.filter(), state=[CreatePass.create_pass, SavePass.choose_pass])
async def on_choose_len_pass(cq: types.CallbackQuery, state: FSMContext, callback_data: dict[str, Any]):
    current_state = await state.get_state()

    if current_state == 'CreatePass:create_pass':
        len_pass = int(callback_data['len'])
        await state.update_data(len_pass=len_pass)

        pwo = PasswordGenerator()
        pwo.minlen = len_pass
        pwo.maxlen = len_pass
        password = pwo.generate()

        try:

            msg_for_user = Blanks.get_create_pass(password=password,
                                                  len_pass=len_pass)

            await cq.message.edit_text(text=msg_for_user,
                                       reply_markup=InlineKb.generation_control(password=password,
                                                                                choose_len_pass=len_pass))
        except CantParseEntities:

            len_pass = int(callback_data['len'])
            await state.update_data(len_pass=len_pass)

            pwo = PasswordGenerator()
            pwo.minlen = len_pass
            pwo.maxlen = len_pass
            password = pwo.generate()

            msg_for_user = Blanks.get_create_pass(password=password,
                                                  len_pass=len_pass)

            await cq.message.edit_text(text=msg_for_user,
                                       reply_markup=InlineKb.generation_control(password=password,
                                                                                choose_len_pass=len_pass))

    else:
        len_pass = int(callback_data['len'])
        await state.update_data(len_pass=len_pass)

        pwo = PasswordGenerator()
        pwo.minlen = len_pass
        pwo.maxlen = len_pass
        password = pwo.generate()

        try:

            msg_for_user = Blanks.get_create_pass(password=password,
                                                  len_pass=len_pass)

            await cq.message.edit_text(text=msg_for_user,
                                       reply_markup=InlineKb.generation_control_for_save_pass(choose_len_pass=len_pass))

        except CantParseEntities:

            len_pass = int(callback_data['len'])
            await state.update_data(len_pass=len_pass)

            pwo = PasswordGenerator()
            pwo.minlen = len_pass
            pwo.maxlen = len_pass
            password = pwo.generate()

            msg_for_user = Blanks.get_create_pass(password=password,
                                                  len_pass=len_pass)

            await cq.message.edit_text(text=msg_for_user,
                                       reply_markup=InlineKb.generation_control_for_save_pass(choose_len_pass=len_pass))
