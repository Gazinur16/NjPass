from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from blanks import Blanks


class InlineKb:
    # MENU_BTN
    cd_but_create_msr_key = CallbackData(f'input_create_msr_key')

    cd_but_len_pass = CallbackData(f'input_len_pass', 'len')
    cd_but_update_pass = CallbackData(f'input_update_pass')
    cd_but_close = CallbackData(f'input_close')
    cd_but_skip_login = CallbackData(f'input_skip_login')
    cd_but_skip_description = CallbackData(f'input_skip_description')

    cd_but_create_pass_or_mine_pass = CallbackData(f'input_create_pass', 'ans')
    cd_but_use_pass = CallbackData(f'input_use_pass')

    cd_but_user_pass = CallbackData(f'input_user_pass', 'id', 'page')
    cd_but_control = CallbackData(f'input_control', 'page')

    cd_but_back_list_pass = CallbackData(f'input_back_list_pass', 'page')
    cd_but_change_pass = CallbackData(f'input_change_pass', 'id')
    cd_but_del_pass = CallbackData(f'input_del_pass', 'id', 'page')

    @classmethod
    def create_msr_key(cls):
        kb = InlineKeyboardMarkup(row_width=1)

        kb.row(InlineKeyboardButton(
            text=Blanks.create_msr_key,
            callback_data=cls.cd_but_create_msr_key.new())
        )

        return kb

    @classmethod
    def send_the_key(cls, msr_key: str):
        kb = InlineKeyboardMarkup(row_width=1)

        kb.insert(InlineKeyboardButton('↪️ Переслать в другой чат', switch_inline_query=msr_key))

        return kb

    @classmethod
    def close_window(cls):
        kb = InlineKeyboardMarkup(row_width=1)

        kb.row(InlineKeyboardButton(
            text=Blanks.close,
            callback_data=cls.cd_but_close.new())
        )

        return kb

    @classmethod
    def skip_login(cls):
        kb = InlineKeyboardMarkup(row_width=1)

        kb.row(InlineKeyboardButton(
            text=Blanks.skip,
            callback_data=cls.cd_but_skip_login.new())
        )

        return kb

    @classmethod
    def skip_description(cls):
        kb = InlineKeyboardMarkup(row_width=1)

        kb.row(InlineKeyboardButton(
            text=Blanks.skip,
            callback_data=cls.cd_but_skip_description.new())
        )

        return kb

    @classmethod
    def choose_gen_pass_or_my_pass(cls):
        kb = InlineKeyboardMarkup(row_width=1)

        kb.row(InlineKeyboardButton(
            text=Blanks.create_pass,
            callback_data=cls.cd_but_create_pass_or_mine_pass.new(ans='create'))
        )

        kb.row(InlineKeyboardButton(
            text=Blanks.input_my_pass,
            callback_data=cls.cd_but_create_pass_or_mine_pass.new(ans='mine'))
        )

        return kb

    @classmethod
    def control_my_pass(cls, pass_data: str, page: int, id_pass: int):
        kb = InlineKeyboardMarkup(row_width=2)

        kb.row(InlineKeyboardButton(
            text='⬅️ Назад',
            callback_data=cls.cd_but_back_list_pass.new(page=page))
        )

        kb.insert(InlineKeyboardButton('↪️ Поделится', switch_inline_query=pass_data))

        kb.row(InlineKeyboardButton(
            text='✏️ Изменить',
            callback_data=cls.cd_but_change_pass.new(id=id_pass))
        )

        kb.insert(InlineKeyboardButton(
            text='🗑 Удалить',
            callback_data=cls.cd_but_del_pass.new(id=id_pass, page=page))
        )

        kb.row(InlineKeyboardButton(
            text=Blanks.cancel,
            callback_data=cls.cd_but_close.new())
        )

        return kb

    @classmethod
    def generation_control(cls, password: str, choose_len_pass: int):
        kb = InlineKeyboardMarkup(row_width=4)

        kb.row(InlineKeyboardButton(
            text=Blanks.update,
            callback_data=cls.cd_but_update_pass.new())
        )

        kb.insert(InlineKeyboardButton('↪️ Переслать', switch_inline_query=password))

        kb.row(InlineKeyboardButton(
            text=Blanks.index_len_pass(choose_len_pass, 8),
            callback_data=cls.cd_but_len_pass.new(len=8))
        )

        kb.insert(InlineKeyboardButton(
            text=Blanks.index_len_pass(choose_len_pass, 12),
            callback_data=cls.cd_but_len_pass.new(len=12))
        )

        kb.insert(InlineKeyboardButton(
            text=Blanks.index_len_pass(choose_len_pass, 16),
            callback_data=cls.cd_but_len_pass.new(len=16))
        )

        kb.insert(InlineKeyboardButton(
            text=Blanks.index_len_pass(choose_len_pass, 24),
            callback_data=cls.cd_but_len_pass.new(len=24))
        )

        kb.row(InlineKeyboardButton(
            text=Blanks.close,
            callback_data=cls.cd_but_close.new())
        )

        return kb

    @classmethod
    def generation_control_for_save_pass(cls, choose_len_pass: int):
        kb = InlineKeyboardMarkup(row_width=4)

        kb.row(InlineKeyboardButton(
            text=Blanks.update,
            callback_data=cls.cd_but_update_pass.new())
        )

        kb.insert(InlineKeyboardButton(
            text=Blanks.use_pass,
            callback_data=cls.cd_but_use_pass.new())
        )

        kb.row(InlineKeyboardButton(
            text=Blanks.index_len_pass(choose_len_pass, 8),
            callback_data=cls.cd_but_len_pass.new(len=8))
        )

        kb.insert(InlineKeyboardButton(
            text=Blanks.index_len_pass(choose_len_pass, 12),
            callback_data=cls.cd_but_len_pass.new(len=12))
        )

        kb.insert(InlineKeyboardButton(
            text=Blanks.index_len_pass(choose_len_pass, 16),
            callback_data=cls.cd_but_len_pass.new(len=16))
        )

        kb.insert(InlineKeyboardButton(
            text=Blanks.index_len_pass(choose_len_pass, 24),
            callback_data=cls.cd_but_len_pass.new(len=24))
        )

        return kb

    @classmethod
    def show_pass_for_user(cls, all_user_pass: list, page: int = 0):

        ITEMS_PAGE = 10  # количество элементов на странице

        kb = InlineKeyboardMarkup(row_width=2)

        # Определение начала и конца среза
        start = page * ITEMS_PAGE
        end = start + ITEMS_PAGE

        # Добавление кнопок для каждого элемента на текущей странице
        for item in all_user_pass[start:end]:
            kb.insert(InlineKeyboardButton(
                text='🔓 '+item[1],
                callback_data=cls.cd_but_user_pass.new(id=item[0], page=page))
            )

        # Добавление кнопок "Назад" и "Вперед", если они необходимы

        if page > 0:  # если конец
            kb.row(InlineKeyboardButton(
                text="⬅️ Назад",
                callback_data=cls.cd_but_control.new(page=page - 1))
            )

        if end < len(all_user_pass):  # если начало
            kb.row(InlineKeyboardButton(
                text="Далее ➡️",
                callback_data=cls.cd_but_control.new(page=page + 1))
            )

        kb.row(InlineKeyboardButton(
            text=Blanks.close,
            callback_data=cls.cd_but_close.new())
        )

        return kb


class StaticKb:
    @classmethod
    def put_user_main_menu(cls):
        kb = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

        kb.add(KeyboardButton(Blanks.create_pass))
        kb.add(KeyboardButton(Blanks.save_pass))
        kb.add(KeyboardButton(Blanks.my_pass))

        return kb
