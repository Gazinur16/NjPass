from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from blanks import Blanks


class InlineKb:
    # MENU_BTN
    cd_but_about_us = CallbackData(f'input_about_us')
    cd_but_our_services = CallbackData(f'input_our_services')
    cd_but_portfolio = CallbackData(f'input_portfolio')
    cd_but_order_consultation = CallbackData(f'input_order_consultation')
    cd_but_invite_a_friend = CallbackData(f'input_invite_a_friend')

    # ABOUT_US_BTN
    cd_but_main_menu = CallbackData(f'input_main_menu')
    cd_but_back = CallbackData(f'input_back', 'state')
    cd_but_about_developer = CallbackData(f'input_about_developer')
    cd_but_about_manager = CallbackData(f'input_about_manager')

    @classmethod
    def show_user_menu(cls):
        kb = InlineKeyboardMarkup(row_width=2)

        kb.row(InlineKeyboardButton(
            text=Blanks.about_bot,
            url='https://telegra.ph/Kto-takie-ehti-vashi-telegramm-boty-09-07',
            callback_data=None)
        )

        kb.row(InlineKeyboardButton(
            text=Blanks.about_us,
            callback_data=cls.cd_but_about_us.new())
        )

        kb.insert(InlineKeyboardButton(
            text=Blanks.our_services,
            callback_data=cls.cd_but_our_services.new())
        )

        kb.row(InlineKeyboardButton(
            text=Blanks.portfolio,
            callback_data=cls.cd_but_portfolio.new())
        )

        kb.insert(InlineKeyboardButton(
            text=Blanks.invite_a_friend,
            callback_data=cls.cd_but_invite_a_friend.new())
        )

        kb.row(InlineKeyboardButton(
            text=Blanks.order_consultation,
            callback_data=cls.cd_but_order_consultation.new())
        )

        kb.row(InlineKeyboardButton(
            text=Blanks.order_a_bot,
            url='https://t.me/Nurka_kari',
            callback_data=None
        ))

        kb.row(InlineKeyboardButton(
            text=Blanks.contact,
            url='https://t.me/NjminOS',
            callback_data=None
        ))

        kb.insert(InlineKeyboardButton(
            text=Blanks.reviews,
            url='https://t.me/+dHteZ6zIan03YmQy',
            callback_data=None
        ))

        return kb

    @classmethod
    def show_about_me_menu(cls):
        kb = InlineKeyboardMarkup(row_width=2)

        kb.row(InlineKeyboardButton(
            text=Blanks.main_menu,
            callback_data=cls.cd_but_main_menu.new())
        )

        kb.row(InlineKeyboardButton(
            text=Blanks.about_developer,
            callback_data=cls.cd_but_about_developer.new())
        )

        return kb

    @classmethod
    def show_about_nurka_menu(cls):
        kb = InlineKeyboardMarkup(row_width=2)

        kb.row(InlineKeyboardButton(
            text=Blanks.main_menu,
            callback_data=cls.cd_but_main_menu.new())
        )

        kb.row(InlineKeyboardButton(
            text=Blanks.about_manager,
            callback_data=cls.cd_but_about_manager.new())
        )

        return kb


class StaticKb:
    @classmethod
    def put_user_main_menu(cls):
        kb = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        kb.add(KeyboardButton(Blanks.user_menu))

        return kb
