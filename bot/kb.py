from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from blanks import Blanks


class InlineKb:
    # MENU_BTN
    cd_but_create_msr_key = CallbackData(f'input_create_msr_key')

    cd_but_len_pass = CallbackData(f'input_len_pass', 'len')
    cd_but_save_generate_pass = CallbackData(f'input_save_generate_pass')
    cd_but_update_pass = CallbackData(f'input_update_pass')
    cd_but_close = CallbackData(f'input_close')
    cd_but_skip_login = CallbackData(f'input_skip_login')

    cd_but_create_pass_or_mine_pass = CallbackData(f'input_create_pass', 'ans')
    cd_but_use_pass = CallbackData(f'input_use_pass')
    # cd_but_ = CallbackData(f'input_')

    @classmethod
    def create_msr_key(cls):
        kb = InlineKeyboardMarkup(row_width=1)

        kb.row(InlineKeyboardButton(
            text=Blanks.create_msr_key,
            callback_data=cls.cd_but_create_msr_key.new())
        )

        return kb

    @classmethod
    def send_the_key(cls, msr_key: bytes):
        kb = InlineKeyboardMarkup(row_width=1)

        kb.insert(InlineKeyboardButton('↪️ Переслать в другой чат', switch_inline_query=str(msr_key)))

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

        kb.insert(InlineKeyboardButton(
            text=Blanks.save,
            callback_data=cls.cd_but_save_generate_pass.new())
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

    # @classmethod
    # def show_about_me_menu(cls):
    #     kb = InlineKeyboardMarkup(row_width=2)
    #
    #     kb.row(InlineKeyboardButton(
    #         text=Blanks.main_menu,
    #         callback_data=cls.cd_but_main_menu.new())
    #     )
    #
    #     kb.row(InlineKeyboardButton(
    #         text=Blanks.about_developer,
    #         callback_data=cls.cd_but_about_developer.new())
    #     )
    #
    #     return kb


class StaticKb:
    @classmethod
    def put_user_main_menu(cls):
        kb = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

        kb.add(KeyboardButton(Blanks.create_pass))
        kb.add(KeyboardButton(Blanks.save_pass))
        kb.add(KeyboardButton(Blanks.my_pass))

        return kb
