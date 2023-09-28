import asyncio
import time
from typing import Any

import cryptography
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import CantParseEntities, MessageNotModified
from cryptography.fernet import Fernet
from password_generator import PasswordGenerator

import kb
from services import del_new_msr_key, del_list_pass
from state import CreatePass, SavePass, MyPass, ResetBot
from kb import InlineKb, StaticKb

from blanks import Blanks
from misc import dp, db, bot

"""COMMAND HANDLERS"""


@dp.message_handler(commands=['start'])
async def start_handler(m: types.Message, state: FSMContext):
    if db.user_exists(m.from_user.id) is False:
        await m.answer_sticker(sticker='CAACAgIAAxkBAAEKZ6dlFLU7JmpcRryamIg-RJ8UfawJ_AACAQEAAladvQoivp8OuMLmNDAE')
        await m.answer(text=Blanks.hello_new_user,
                       reply_markup=InlineKb.create_msr_key())
    else:
        await m.answer_sticker(sticker='CAACAgIAAxkBAAEKZ6dlFLU7JmpcRryamIg-RJ8UfawJ_AACAQEAAladvQoivp8OuMLmNDAE')
        await m.answer(text=Blanks.hello_old_user,
                       reply_markup=StaticKb.put_user_main_menu())

    await state.finish()


@dp.message_handler(commands=['reset'])
async def reset_handler(m: types.Message, state: FSMContext):
    await m.answer_sticker(sticker='CAACAgIAAxkBAAEKZ6tlFLjfCpxtKNnu-g7hDTixoiQZvAACSAIAAladvQoc9XL43CkU0DAE')
    await m.answer(text=Blanks.reset_Bot, reply_markup=StaticKb.put_user_btn_menu())

    await ResetBot.input_yes.set()


# @dp.message_handler(commands=['help'])
# async def help_handler(m: types.Message):
#     await m.answer('Hello')


"""MESSAGE HANDLERS"""


@dp.message_handler(text=Blanks.user_menu, state="*")
async def on_menu(m: types.Message, state: FSMContext):
    data = await state.get_data()
    last_inline_btn = data.get("last_inline_btn")

    try:
        await bot.delete_message(chat_id=last_inline_btn.chat.id, message_id=last_inline_btn.message_id)
    except MessageNotModified:
        pass
    except AttributeError:
        pass

    await m.answer_sticker(sticker='CAACAgIAAxkBAAEKZ6llFLdNJTTEoHuMUa5sJhKEQcmcSQACTgIAAladvQow_mttgTIDbzAE',
                           reply_markup=StaticKb.put_user_main_menu())
    # await m.answer(text=Blanks.choose_option_menu, reply_markup=StaticKb.put_user_main_menu())

    await state.finish()


@dp.message_handler(state=ResetBot.input_yes)
async def check_reset_bot(m: types.Message, state: FSMContext):
    if m.text == 'Сбросить бота':
        db.del_user(m.from_user.id)  # удаление пользователя

        await m.answer(text=Blanks.hello_new_user,
                       reply_markup=InlineKb.create_msr_key())

    else:
        await m.answer(text=f'Чтобы вернуться, нажмите на кнопку {Blanks.user_menu}',
                       reply_markup=StaticKb.put_user_btn_menu())


@dp.message_handler(text=Blanks.my_pass)
async def on_my_pass(m: types.Message):
    await m.answer(text=Blanks.input_msr_key_for_decode)

    await MyPass.input_msr_key.set()


@dp.message_handler(state=MyPass.input_msr_key)
async def input_msr_key(m: types.Message, state: FSMContext):
    try:
        encode_one_pass_user = db.check_msr_key(m.from_user.id)[0][0]

        key = m.text.encode()
        await state.update_data(msr_key=key)
        cipher_suite = Fernet(key)  # Инициализация объекта Fernet c Мастер-Ключем

        # Дешифрование
        bytes_pass = cipher_suite.decrypt(encode_one_pass_user)
        decode_pass = bytes_pass.decode()

        await m.delete()
        list_pass = db.get_name_pass_user(m.from_user.id)
        sorted_list_pass = sorted(list_pass, key=lambda x: x[1])

        await m.answer_sticker(sticker='CAACAgIAAxkBAAEKZ6NlFLQPOZs0RbtXzTwg4FDkRIzkEQAC_gADVp29CtoEYTAu-df_MAQ',
                               reply_markup=StaticKb.put_user_btn_menu())

        await state.update_data(time_now=time.monotonic())
        list_pass_mes = await m.answer(text=Blanks.you_list_pass(120),
                                       reply_markup=InlineKb.show_pass_for_user(sorted_list_pass))

        await state.update_data(last_inline_btn=list_pass_mes)
        await del_list_pass(chat_id=list_pass_mes.chat.id, mes_id=list_pass_mes.message_id, start_time=time.monotonic())

    except cryptography.fernet.InvalidToken:

        await m.answer_sticker(sticker='CAACAgIAAxkBAAEKZ6VlFLQm2EzIPCOL6TJvp7PrPZRq0QACAgEAAladvQpO4myBy0Dk_zAE')
        await m.answer(text=Blanks.invalid_msr_key, reply_markup=StaticKb.put_user_btn_menu())

    except ValueError:
        await m.answer_sticker(sticker='CAACAgIAAxkBAAEKZ6VlFLQm2EzIPCOL6TJvp7PrPZRq0QACAgEAAladvQpO4myBy0Dk_zAE')
        await m.answer(text=Blanks.error_msr_key, reply_markup=StaticKb.put_user_btn_menu())

    except IndexError:
        await m.delete()
        await m.answer_sticker(sticker='CAACAgIAAxkBAAEKZ6FlFLP_wlxZ2f9h1rVJD0JbtfXXuQACSQIAAladvQoqlwydCFMhDjAE')
        await m.answer(text=Blanks.not_list_pass, reply_markup=StaticKb.put_user_btn_menu())


@dp.message_handler(text=Blanks.create_pass)
async def on_create_pass(m: types.Message, state: FSMContext):
    await m.answer(text=Blanks.creating_pass, reply_markup=StaticKb.put_user_btn_menu())

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

        last_inline_btn = await m.answer(text=msg_for_user,
                                         reply_markup=InlineKb.generation_control(password=password,
                                                                                  choose_len_pass=start_len_pass))

        await state.update_data(last_inline_btn=last_inline_btn)

    except CantParseEntities:

        pwo = PasswordGenerator()
        pwo.minlen = start_len_pass
        pwo.maxlen = start_len_pass
        password = pwo.generate()

        msg_for_user = Blanks.get_create_pass(password=password,
                                              len_pass=start_len_pass)

        last_inline_btn = await m.answer(text=msg_for_user,
                                         reply_markup=InlineKb.generation_control(password=password,
                                                                                  choose_len_pass=start_len_pass))
        await state.update_data(last_inline_btn=last_inline_btn)


@dp.message_handler(text=Blanks.save_pass)
async def on_save_pass(m: types.Message):
    await m.answer(text=Blanks.input_name_pass, reply_markup=StaticKb.put_user_btn_menu())

    await SavePass.input_name_pass.set()


@dp.message_handler(state=SavePass.input_name_pass)
async def save_name_pass(m: types.Message, state: FSMContext):
    if len(m.text) < 15:
        await state.update_data(name_pass=m.text)

        mes_login = await m.answer(text=Blanks.input_login,
                                   reply_markup=InlineKb.skip_login())

        await state.update_data(mes_login=mes_login)
        await state.update_data(last_inline_btn=mes_login)

        await SavePass.next()
    else:
        await m.answer(text=Blanks.big_len_name_pass)


@dp.message_handler(state=SavePass.input_login)
async def save_login(m: types.Message, state: FSMContext):
    try:
        data = await state.get_data()
        mes_login = data.get("mes_login")

        await bot.edit_message_reply_markup(chat_id=mes_login.chat.id,  # удаляем инлайн кнопку у предыдущего сообщения
                                            message_id=mes_login.message_id,
                                            reply_markup=None)
    except MessageNotModified:
        pass

    await state.update_data(login=m.text)
    # await m.delete()
    # await m.answer(text=Blanks.hide_user_input_data)

    await m.answer(text=Blanks.choose_gen_pass_or_my_pass,
                   reply_markup=InlineKb.choose_gen_pass_or_my_pass())

    await SavePass.next()


@dp.message_handler(state=SavePass.input_pass)
async def save_pass(m: types.Message, state: FSMContext):
    await state.update_data(last_pass=m.text)

    await m.delete()
    await m.answer(text=Blanks.hide_user_input_data)

    mes_description = await m.answer(text=Blanks.input_description,
                                     reply_markup=InlineKb.skip_description())
    await state.update_data(last_inline_btn=mes_description)

    await state.update_data(mes_description=mes_description)

    await SavePass.next()


@dp.message_handler(state=SavePass.input_description)
async def save_description(m: types.Message, state: FSMContext):
    data = await state.get_data()
    mes_description = data.get("mes_description")

    await bot.edit_message_reply_markup(chat_id=mes_description.chat.id,
                                        message_id=mes_description.message_id,
                                        reply_markup=None)

    await state.update_data(description=m.text)
    # await m.delete()
    # await m.answer(text=Blanks.hide_user_input_data)

    await m.answer(text=Blanks.input_msr_key_for_encode)

    await SavePass.next()


@dp.message_handler(state=SavePass.input_msr_key)
async def save_new_password(m: types.Message, state: FSMContext):
    data = await state.get_data()
    name_pass = data.get("name_pass")
    login = data.get("login")
    last_pass = data.get("last_pass")
    description = data.get("description")

    try:
        key = m.text.encode()
        cipher_suite = Fernet(key)  # Инициализация объекта Fernet c Мастер-Ключем

        # Шифрование
        bytes_last_pass = last_pass.encode()
        encode_pass = cipher_suite.encrypt(bytes_last_pass)

        if login is not None:
            bytes_login = login.encode()
            encode_login = cipher_suite.encrypt(bytes_login)
        else:
            encode_login = login

        if description is not None:
            bytes_description = description.encode()
            encode_description = cipher_suite.encrypt(bytes_description)
        else:
            encode_description = description

        db.add_pass_for_user(tg_id=m.from_user.id, name_pass=name_pass, login=encode_login,
                             password=encode_pass, description=encode_description)

        await m.delete()
        await m.answer_sticker(sticker='CAACAgIAAxkBAAEKZ6FlFLP_wlxZ2f9h1rVJD0JbtfXXuQACSQIAAladvQoqlwydCFMhDjAE')
        await m.answer(text=Blanks.success_msr_key, reply_markup=StaticKb.put_user_main_menu())

        await state.finish()

    except ValueError:
        await m.answer_sticker(sticker='CAACAgIAAxkBAAEKZ6VlFLQm2EzIPCOL6TJvp7PrPZRq0QACAgEAAladvQpO4myBy0Dk_zAE')
        await m.answer(text=Blanks.error_msr_key, reply_markup=StaticKb.put_user_btn_menu())


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

    last_inline_btn = await cq.message.edit_text(text=Blanks.choose_gen_pass_or_my_pass,
                                                 reply_markup=InlineKb.choose_gen_pass_or_my_pass())
    await state.update_data(last_inline_btn=last_inline_btn)

    await SavePass.next()


@dp.callback_query_handler(kb.InlineKb.cd_but_skip_description.filter(), state=SavePass.input_description)
async def on_skip_description(cq: types.CallbackQuery, state: FSMContext):
    await state.update_data(description=None)

    await cq.message.edit_text(text=Blanks.input_msr_key_for_encode)

    await SavePass.next()


@dp.callback_query_handler(kb.InlineKb.cd_but_continue_see_pass.filter(), state=MyPass.input_msr_key)
async def on_continue_see_pass(cq: types.CallbackQuery, state: FSMContext):
    await state.finish()

    await cq.message.edit_text(text=Blanks.input_msr_key_for_decode, reply_markup=None)

    await MyPass.input_msr_key.set()


@dp.callback_query_handler(kb.InlineKb.cd_but_control.filter(), state=MyPass.input_msr_key)
async def on_action_btn(cq: types.CallbackQuery, callback_data: dict[str, Any], state: FSMContext):
    page = int(callback_data['page'])

    list_pass = db.get_name_pass_user(cq.from_user.id)
    sorted_list_pass = sorted(list_pass, key=lambda x: x[1])

    data = await state.get_data()
    time_now = data.get("time_now")

    await cq.message.edit_text(text=Blanks.you_list_pass(120 - int(time.monotonic() - time_now)),
                               reply_markup=InlineKb.show_pass_for_user(sorted_list_pass, page))


@dp.callback_query_handler(kb.InlineKb.cd_but_back_list_pass.filter(), state=MyPass.input_msr_key)
async def on_back_list_pass(cq: types.CallbackQuery, callback_data: dict[str, Any], state: FSMContext):
    page = int(callback_data['page'])

    list_pass = db.get_name_pass_user(cq.from_user.id)
    sorted_list_pass = sorted(list_pass, key=lambda x: x[1])

    data = await state.get_data()
    time_now = data.get("time_now")

    await cq.message.edit_text(text=Blanks.you_list_pass(120 - int(time.monotonic() - time_now)),
                               reply_markup=InlineKb.show_pass_for_user(sorted_list_pass, page))


@dp.callback_query_handler(kb.InlineKb.cd_but_del_pass.filter(), state=MyPass.input_msr_key)
async def on_del_pass_user(cq: types.CallbackQuery, callback_data: dict[str, Any], state: FSMContext):
    id_pass = int(callback_data['id'])
    page = int(callback_data['page'])

    db.del_pass_user(id_pass)  # удаление пароля
    await cq.answer(text='🗑 Пароль удален', show_alert=True)

    list_pass = db.get_name_pass_user(cq.from_user.id)
    sorted_list_pass = sorted(list_pass, key=lambda x: x[1])

    data = await state.get_data()
    time_now = data.get("time_now")

    await cq.message.edit_text(text=Blanks.you_list_pass(120 - int(time.monotonic() - time_now)),
                               reply_markup=InlineKb.show_pass_for_user(sorted_list_pass, page))


@dp.callback_query_handler(kb.InlineKb.cd_but_user_pass.filter(), state=MyPass.input_msr_key)
async def on_user_pass(cq: types.CallbackQuery, state: FSMContext, callback_data: dict[str, Any]):
    data = await state.get_data()
    msr_key = data.get("msr_key")

    id_pass = int(callback_data['id'])
    page = int(callback_data['page'])

    user_pass = db.get_pass_user(id_pass)[0]  # получаем зашифрованные данные из БД

    name_pass = user_pass[0]
    encode_login = user_pass[1]
    encode_pass_user = user_pass[2]
    encode_description = user_pass[3]

    cipher_suite = Fernet(msr_key)  # Инициализация объекта Fernet c Мастер-Ключем

    # Дешифрование
    bytes_pass = cipher_suite.decrypt(encode_pass_user)
    decode_pass = bytes_pass.decode()

    if encode_login is not None:
        bytes_login = cipher_suite.decrypt(encode_login)
        decode_login = bytes_login.decode()
    else:
        decode_login = encode_login

    if encode_description is not None:
        bytes_description = cipher_suite.decrypt(encode_description)
        decode_description = bytes_description.decode()
    else:
        decode_description = encode_description

    pass_for_user = Blanks.get_pass_user(name_pass=name_pass, decode_login=decode_login,
                                         decode_pass=decode_pass, decode_description=decode_description)

    send_pass_user = Blanks.send_pass_user(name_pass=name_pass, decode_login=decode_login,
                                           decode_pass=decode_pass, decode_description=decode_description)

    # await cq.answer(text=Blanks.hide_list_pass, show_alert=True)

    await cq.message.edit_text(text=pass_for_user,
                               reply_markup=InlineKb.control_my_pass(pass_data=send_pass_user,
                                                                     page=page,
                                                                     id_pass=id_pass))


@dp.callback_query_handler(kb.InlineKb.cd_but_use_pass.filter(), state=SavePass.choose_pass)
async def on_use_pass(cq: types.CallbackQuery, state: FSMContext):
    mes_description = await cq.message.edit_text(text=Blanks.input_description,
                                                 reply_markup=InlineKb.skip_description())

    await state.update_data(mes_description=mes_description)
    await state.update_data(last_inline_btn=mes_description)

    await SavePass.input_description.set()


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

        await state.update_data(last_pass=password)

        last_inline_btn = await cq.message.edit_text(
            text=Blanks.get_create_pass(password=password, len_pass=start_len_pass),
            reply_markup=InlineKb.generation_control_for_save_pass(
                choose_len_pass=start_len_pass))

        await state.update_data(last_inline_btn=last_inline_btn)

    else:
        await cq.message.edit_text(text=Blanks.input_pass)

        await SavePass.next()


@dp.callback_query_handler(kb.InlineKb.cd_but_create_msr_key.filter(), state="*")
async def on_create_msr_key(cq: types.CallbackQuery, state: FSMContext):
    await cq.message.edit_reply_markup(None)

    if db.user_exists(cq.from_user.id) is False:

        db.add_user(tg_id=cq.from_user.id)

        key = str(Fernet.generate_key())[2:-1]  # создание Мастер-Ключа

        await cq.message.answer_sticker(
            sticker='CAACAgIAAxkBAAEKZ6FlFLP_wlxZ2f9h1rVJD0JbtfXXuQACSQIAAladvQoqlwydCFMhDjAE',
            reply_markup=StaticKb.put_user_main_menu())

        await cq.message.answer(
            text=Blanks.get_create_msr_key(key),
            reply_markup=InlineKb.send_the_key(key)
        )

        await state.finish()

        # небольшой воркер
        start_time = time.monotonic()
        asyncio.create_task(del_new_msr_key(cq.message.chat.id, cq.message.message_id, start_time))

    else:
        await cq.message.edit_text(
            text=Blanks.no_save_msr_key,
            reply_markup=None
        )


@dp.callback_query_handler(kb.InlineKb.cd_but_close.filter(), state="*")
async def on_close_win(cq: types.CallbackQuery, state: FSMContext):
    await cq.message.edit_text(
        text=Blanks.closet
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

            await state.update_data(last_pass=password)

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

            await state.update_data(last_pass=password)

            msg_for_user = Blanks.get_create_pass(password=password,
                                                  len_pass=len_pass)

            await cq.message.edit_text(text=msg_for_user,
                                       reply_markup=InlineKb.generation_control_for_save_pass(choose_len_pass=len_pass))
