class Blanks:
    # HELLO
    hello_new_user = 'Приветвую вас в <b>NjPass</b> 👾\n\n' \
                     'Тут вы сможете создавать и безопасно хранить <b><i>Ваши</i></b> пароли 🔒\n\n' \
                     'Для начала нужно создать <u>Мастер-Ключ</u> 🔑\n' \
                     'Он нужен для зашифровки и расшифровки ваших паролей 💾\n\n' \
                     'Бот не будет хранить его и досту к ключам будет только у Вас 💫'

    hello_old_user = 'С возвращением в <b>NjPass</b> 👾\n\n' \
                     'Тут <b><i>Ваши</i></b> пароли в безопасности 🔒'

    reset_Bot = 'В случае, если вы <b>забыли свой Мастер-Ключ</b> 🔑\n\n' \
                'Можно начать пользоваться ботом заново, однако <u>ВСЕ ВАШИ ПРЕДЫДУЩИЕ ПАРОЛИ БУДУТ УТЕРЯНЫ</u> ❌\n\n' \
                'Администартор НЕ МОЖЕТ восстановить ваш доступ, так-как все ваши пароли <b>зашифрованы</b> 🔒\n\n' \
                '👾 Чтобы сбросить бота наберите сюда фразу "<code>Сбросить бота</code>": '

    update = '🔄 Обновить'
    use_pass = '➡️ Использовать'
    closet = '👾 Выберите действие в <b>меню</b>:'
    save = '💾 Сохрнаить'
    skip = '➡️ Пропустить'

    user_menu = '🗂 В меню'
    choose_option_menu = '👾 Выберите действие в меню:'
    create_pass = '🔑 Сгенерировать пароль'
    creating_pass = '👾 Генерация пароля...'
    input_my_pass = '✏️ Ввести свой пароль'
    save_pass = '🔏 Создать и сохранить пароль'
    my_pass = '🔒 Мои сохраненные пароли'
    not_list_pass = 'У вас нет сохраненных паролей ☝️'

    create_msr_key = '🔐 Сгенерировать Мастер-Ключ'
    no_save_msr_key = '<b>Мастер-Ключ</b> ключ уже создан ⚠️'

    hide_user_input_data = '👁‍🗨 Введеный пароль был скрыт в целях <b>безопасности</b>'
    hide_list_pass = '⚠️ Окно будет скрыто через 1 минуту'

    input_name_pass = 'Введите <b>наименование пароля</b>\n(15 символов) 🔖'
    big_len_name_pass = 'Введеное вами наименование <b>превышает 15 символов</b> ⚠️\n\n' \
                        'Попробуйте ввести снова 🔖'

    input_login = 'Введите <b>логин</b> от сервиса 👤'

    choose_gen_pass_or_my_pass = '👾 Вы хотите <b>сгенерировать пароль</b>, или ввести его <b>самостоятельно</b>?'
    input_pass = 'Введите <b>пароль</b> от сервиса 🔐'

    input_description = 'Введите <b>описание/доп.информацию</b> для пароля 📎'

    input_msr_key_for_encode = 'Введите <b>Мастер-Ключ</b> для зашифровки пароля 🔑'
    input_msr_key_for_decode = 'Введите свой <b>Мастер-Ключ</b> для расшифровки паролей 🔑'

    success_msr_key = '<b>Пароль зашифрован и сохранен</b>🔒\n\n' \
                      'Для просмотре <b>Ваших</b> паролей используйте тот-же <b>Мастер-Ключ</b> 🔑'

    correct_msr_key = '🔓 Корректный <b>Мастер-Ключ</b>'

    error_msr_key = '⚠️ Неправильный формат <b>Мастер-Ключа</b>\n\n' \
                    'Попробуйте ввести его снова 🔑'

    invalid_msr_key = '⚠️ Неправильный <b>Мастер-Ключ</b>\n\n' \
                      'Попробуйте ввести его снова 🔑'

    @classmethod
    def get_create_msr_key(cls, msr_key: str) -> str:
        create_msr_key = '🔐  Ват ваш личный <b>Мастер-Ключ</b>:\n\n' \
                         f'<code>{msr_key}</code>\n\n' \
                         'Позаботьтесь о его сохранности, ' \
                         'иначе вы <b><i>навсегда потеряйете</i></b> досту к своим паролям ☝️\n\n' \
                         '⚠️ Данное сообщение будет <b>удалено через 3 минуты</b> в целях безопасности\n\n' \
                         'Вы можете:\n' \
                         '- кликнуть на ключ, чтобы скопировать его 🔗\n' \
                         '- переслать ключ в другой чат ↪️'

        return create_msr_key

    @classmethod
    def get_create_pass(cls, password: str, len_pass: int) -> str:
        create_pass = f'Сгенерирован {len_pass}-значный пароль:\n\n' \
                      f'🔐 <code>{password}</code>\n\n' \
                      f'Кликните, чтобы скопировать ☝️'

        return create_pass

    @classmethod
    def you_list_pass(cls, time: int) -> str:
        return f'💾 Ваши сохраненные пароли:\n\n' \
               f'Окно удалится через {time} сек. ⌛️'

    @classmethod
    def get_pass_user(cls, name_pass: str, decode_login: str, decode_pass: str, decode_description: str) -> str:
        user_pass = f'🏷 Данные пароля <b>"{name_pass}"</b>\n\n' \
                    f'👤 Логин: <code>{decode_login}</code>\n' \
                    f'🔐 Пароль: <code>{decode_pass}</code>\n\n'
        if decode_description is not None:
            user_pass += f'📎 <i>Доп. информация</i> к паролю: \n' \
                         f'<code>{decode_description}</code>'
        else:
            pass

        return user_pass

    @classmethod
    def send_pass_user(cls, name_pass: str, decode_login: str, decode_pass: str, decode_description: str) -> str:
        user_pass = f'\n\n🏷 Данные пароля "{name_pass}"\n\n' \
                    f'👤 Логин: {decode_login}\n' \
                    f'🔐 Пароль: {decode_pass}\n\n'

        if decode_description is not None:
            user_pass += f'📎 Доп. информация к паролю: \n' \
                         f'{decode_description}'
        else:
            pass

        return user_pass

    @classmethod
    def index_len_pass(cls, choose_len_pass: int, index_btn: int) -> str:
        if choose_len_pass == index_btn:
            return f'✅ {index_btn}'
        else:
            return f'{index_btn}'

# async def _example1():
#     print(Blanks.message_when_clicked('Заявка на запрос остатков на складе'))
#
#
# if __name__ == '__main__':
#     asyncio.run(_example1())
