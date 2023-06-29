# импорты
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id

from vk_api.keyboard import VkKeyboard, VkKeyboardColor

from config import community_token, access_token
from backend import VkTools
from bd import BdTools
from bd import engine    # ++++++++++++

# отправка сообщений


class BotInterface():
    def __init__(self, community_token, access_token):
        self.vk = vk_api.VkApi(token=community_token)
        self.longpoll = VkLongPoll(self.vk)
        self.vk_tools = VkTools(access_token)
        self.bd_tools = BdTools(engine)       # +++++++++++
        self.check_user = BdTools(engine)     # +++++++++++
        self.params = {}
        self.worksheets = []
        self.offset = 0

    def message_send(self, user_id, message, keyboard, attachment=None):
        self.vk.method('messages.send',
                       {'user_id': user_id,
                        'message': message,
                        'attachment': attachment,
                        'random_id': get_random_id(),
                        'keyboard': keyboard
                        }
                       )

# обработка событий / получение сообщений

    # def event_handler(self):
    #     for event in self.longpoll.listen():
    #
    #         ''''Кнопки'''
    #         buttons = ['Привет', 'Поиск', 'Пока']
    #         button_colors = [VkKeyboardColor.PRIMARY, VkKeyboardColor.PRIMARY, VkKeyboardColor.PRIMARY]
    #         keyboard = self.chat_keyboard(buttons, button_colors)
    #
    #         if event.type == VkEventType.MESSAGE_NEW and event.to_me:
    #             if event.text.lower() == 'привет':
    #                 '''Логика для получения данных о пользователе'''
    #                 self.params = self.vk_tools.get_profile_info(event.user_id)
    #                 self.message_send(event.user_id, f'Привет, {self.params["name"]}', keyboard=keyboard.get_keyboard())
    #                 if self.params is not None:  # Ошибка если инф. не получена
    #                     '''Запрос недостающих данных о пользователе'''
    #
    #                     if not self.params['city']:
    #                         self.message_send(event.user_id, f'Привет, {self.params["name"]}, введите название вашего '
    #                                                          'города проживания:', keyboard=keyboard.get_keyboard())
    #                         while True:
    #                             for event_ in self.longpoll.listen():
    #                                 if event_.type == VkEventType.MESSAGE_NEW and event_.to_me:
    #                                     self.params = self.vk_tools.get_profile_info(event.user_id)
    #                                     self.params['city'] = event_.text
    #                                     break
    #                             if self.params['city']:
    #                                 self.message_send(event.user_id, '---Принято---', keyboard=keyboard.get_keyboard())
    #                                 break
    #
    #                     elif not self.params['sex']:  # чё не срабатывает то второе условие после первого?
    #                         self.message_send(event.user_id, 'Введите ваш пол (м/ж):', keyboard=keyboard.get_keyboard())
    #                         self.params['sex'] = 2 if event.text == 'м' else 1  # ++++++++
    #                         while True:
    #                             for event_ in self.longpoll.listen():
    #                                 if event_.type == VkEventType.MESSAGE_NEW and event_.to_me:
    #                                     self.params = self.vk_tools.get_profile_info(event.user_id)
    #                                     self.params['sex'] = event_.text
    #                                     break
    #                             if self.params['sex']:
    #                                 self.message_send(event.user_id, '---Принято---', keyboard=keyboard.get_keyboard())
    #                                 break
    #
    #                     elif not self.params['year']:   # нужно добавить если год скрыт у пользователя
    #                         self.message_send(event.user_id, 'Введите ваш возраст:', keyboard=keyboard.get_keyboard())
    #                         self.params['year'] = event.text  # ++++++++
    #                         while True:
    #                             for event_ in self.longpoll.listen():
    #                                 if event_.type == VkEventType.MESSAGE_NEW and event_.to_me:
    #                                     self.params = self.vk_tools.get_profile_info(event.user_id)
    #                                     self.params['year'] = event_.text
    #                                     break
    #                             if self.params['year']:
    #                                 self.message_send(event.user_id, '---Принято---', keyboard=keyboard.get_keyboard())
    #                                 break
    #
    #                     elif not self.params['relation'] or self.params['relation']:
    #                         self.params['relation'] = 6  # в активном поиске
    #
    #                     else:
    #                         self.message_send(event.user_id, f'Привет, {self.params["name"]}, нажми "Поиск", '
    #                                                          'чтобы я нашел анкеты', keyboard=keyboard.get_keyboard())
    #                 else:
    #                     self.message_send(event.user_id, 'Ошибка получения данных', keyboard=keyboard.get_keyboard())
    #
    #             elif event.text.lower() == 'поиск':
    #                 '''Логика для поиска анкет'''
    #                 self.message_send(
    #                     event.user_id, 'Идет поиск...', keyboard=keyboard.get_keyboard())
    #                 if self.worksheets:
    #                     worksheet = self.worksheets.pop()
    #                     photos = self.vk_tools.get_photos(worksheet['id'])
    #                     photo_string = ''
    #                     for photo in photos:
    #                         photo_string += f'photo{photo["owner_id"]}_{photo["id"]},'
    #                 else:
    #                     self.worksheets = self.vk_tools.search_worksheet(self.params, self.offset)
    #                     worksheet = self.worksheets.pop()
    #                     self.offset += 50
    #
    #                 '''првоерка анкеты в бд в соотвествие с event.user_id'''
    #                 while self.bd_tools.check_user(event.user_id, worksheet["id"]) is True:  # +++++++
    #                     worksheet = self.worksheets.pop()
    #
    #                 'добавление анкеты в бд в соотвествие с event.user_id'
    #                 if self.bd_tools.check_user(event.user_id, worksheet["id"]) is False:
    #                     self.bd_tools.add_user(event.user_id, worksheet["id"])  # добавление, если нет в базе
    #
    #                     photos = self.vk_tools.get_photos(worksheet['id'])
    #                     photo_string = ''
    #                     for photo in photos:
    #                         photo_string += f'photo{photo["owner_id"]}_{photo["id"]},'
    #
    #                     self.message_send(
    #                         event.user_id,
    #                         f'Имя: {worksheet["name"]}. Страница: vk.com/id{worksheet["id"]}',
    #                         attachment=photo_string, keyboard=keyboard.get_keyboard()
    #                     )
    #
    #             elif event.text.lower() == 'пока':
    #                 self.message_send(
    #                     event.user_id, 'До новых встреч', keyboard=keyboard.get_keyboard())
    #             else:
    #                 self.message_send(
    #                     event.user_id, 'Неизвестная команда', keyboard=keyboard.get_keyboard())

    def event_handler(self):
        for event in self.longpoll.listen():
            '''Кнопки'''
            buttons = ['Привет', 'Поиск', 'Пока']
            button_colors = VkKeyboardColor.PRIMARY, VkKeyboardColor.PRIMARY, VkKeyboardColor.PRIMARY
            keyboard = self.chat_keyboard(buttons, button_colors)

            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                if event.text.lower() == 'привет':
                    self.params = self.vk_tools.get_profile_info(event.user_id)
                    self.params['relation'] = 6  # в активном поиске
                    self.event_greeting(event.user_id, keyboard)
                    if not self.params['city']:
                        self.event_city_input(event.user_id, keyboard)
                    elif not self.params['sex']:
                        self.event_sex_input(event.user_id, keyboard)
                    elif not self.params['year']:
                        self.event_year_input(event.user_id, keyboard)

                elif event.text.lower() == 'поиск' or event.text.lower() == 'далее':
                    '''Логика для поиска анкет'''
                    self.message_send(
                        event.user_id, 'Идет поиск...', keyboard=keyboard.get_keyboard())
                    if self.worksheets:
                        worksheet = self.worksheets.pop()
                        photos = self.vk_tools.get_photos(worksheet['id'])
                        photo_string = ''
                        for photo in photos:
                            photo_string += f'photo{photo["owner_id"]}_{photo["id"]},'
                    else:
                        self.worksheets = self.vk_tools.search_worksheet(self.params, self.offset)
                        worksheet = self.worksheets.pop()
                        self.offset += 50

                    '''првоерка анкеты в бд в соотвествие с event.user_id'''
                    while self.bd_tools.check_user(event.user_id, worksheet["id"]) is True:  # +++++++
                        worksheet = self.worksheets.pop()

                    '''добавление анкеты в бд в соотвествие с event.user_id'''
                    if self.bd_tools.check_user(event.user_id, worksheet["id"]) is False:
                        self.bd_tools.add_user(event.user_id, worksheet["id"])  # добавление, если нет в базе

                        photos = self.vk_tools.get_photos(worksheet['id'])
                        photo_string = ''
                        for photo in photos:
                            photo_string += f'photo{photo["owner_id"]}_{photo["id"]},'

                        self.message_send(
                            event.user_id,
                            f'Имя: {worksheet["name"]}. Страница: vk.com/id{worksheet["id"]}',
                            attachment=photo_string, keyboard=keyboard.get_keyboard()
                        )

                elif event.text.lower() == 'пока':
                    self.message_send(
                        event.user_id, 'До новых встреч', keyboard=keyboard.get_keyboard())
                else:
                    self.message_send(
                        event.user_id, 'Неизвестная команда', keyboard=keyboard.get_keyboard())

    def event_greeting(self, user_id, keyboard):
        self.message_send(user_id, f'Привет, {self.params["name"]}', keyboard=keyboard.get_keyboard())

    def event_city_input(self, user_id, keyboard):
        self.message_send(user_id, 'Введите название вашего города проживания:',
                          keyboard=keyboard.get_keyboard())
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                self.params['city'] = event.text
                break
        if self.params['city']:
            self.message_send(user_id, 'ОК', keyboard=keyboard.get_keyboard())

    def event_sex_input(self, user_id, keyboard):
        self.message_send(user_id, 'Введите ваш пол М - мужской, Ж - женский:', keyboard=keyboard.get_keyboard())
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                self.params['sex'] = event.text
                break
        if self.params['sex']:
            self.message_send(user_id, 'ОК', keyboard=keyboard.get_keyboard())

    def event_year_input(self, user_id, keyboard):
        self.message_send(user_id, 'Введите ваш возраст:', keyboard=keyboard.get_keyboard())
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                self.params['year'] = event.text
                break
        if self.params['year']:
            self.message_send(user_id, 'ОК', keyboard=keyboard.get_keyboard())

    def chat_keyboard(self, buttons, button_colors):
        """Клавиатура"""
        keyboard = VkKeyboard.get_empty_keyboard()
        keyboard = VkKeyboard(one_time=True)
        for btn, btn_color in zip(buttons, button_colors):
            keyboard.add_button(btn, btn_color)
        return keyboard


if __name__ == '__main__':
    bot_interface = BotInterface(community_token, access_token)
    bot_interface.event_handler()
