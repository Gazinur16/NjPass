class Blanks:
    # HELLO
    hello_new_user = 'Приветвую вас в <b>NjPass</b> 👾\n\n' \
                     'Тут вы сможете создавать и безопасно хранить <b><i>Ваши</i></b> пароли 🔒\n\n' \
                     'Для начала нужно создать <u>Мастер-Ключ</u> 🔑\n' \
                     'Он нужен для зашифровки и разшифровки ваших паролей 💾\n\n' \
                     'Бот не будет хранить его и досту к ключам будет только у Вас 💫'

    hello_old_user = 'С возвращением в <b>NjPass</b> 👾\n\n' \
                     'Тут <b><i>Ваши</i></b> пароли в безопасности 🔒'

    update = '🔄 Обновить'
    use_pass = '➡️ Использовать'
    close = '❌ Закрыть'
    closet = '👾 Закрыто...'
    save = '💾 Сохрнаить'
    skip = '➡️ Пропустить'

    create_pass = '🔑 Сгенерировать пароль'
    input_my_pass = '✏️ Ввести свой пароль'
    save_pass = '🔏 Создать и сохранить пароль'
    my_pass = '🔒 Мои сохраненные пароли'

    create_msr_key = '🔐 Создать Мастер-Ключ'
    no_save_msr_key = '<b>Мастер-Ключ</b> ключ уже создан ⚠️'
    # input_my_msr_pass = 'Введите свой <b>Мастер-Ключ</b> ✏️'

    input_name_pass = 'Введите наименование пароля\n(20 символов) 🔖'
    big_len_name_pass = 'Введеное вами наименование <b>превышает 20 символов</b> ⚠️\n\n' \
                        'Попробуйте ввести снова 🔖'

    input_login = 'Введите логин от сервиса (латинские буквы/цифры)👤'
    choose_gen_pass_or_my_pass = '👾 Вы хотите <b>сгенерировать пароль</b>, или ввести его <b>самостоятельно</b>?'
    input_pass = 'Введите пароль от сервиса (латинские буквы/цифры) 🔐'
    # input_pass = 'Введите пароль от сервиса (латинские буквы/цифры) 🔐'
    input_description = 'Введите описание/доп. информацию для пароля 📎'

    @classmethod
    def get_create_msr_key(cls, msr_key: bytes) -> str:
        create_msr_key = '🔐  Ват ваш личный <b>Мастер-Ключ</b>:\n\n' \
                         f'<code>{msr_key}</code>\n\n' \
                         'Позаботьтесь о его сохранности, ' \
                         'иначе вы <b><i>навсегда потеряйете</i></b> досту к своим паролям ☝️\n\n' \
                         '⚠️ Данное сообщение будет <b>удалено через 3 минуты</b> в целях безопасности\n\n'\
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
