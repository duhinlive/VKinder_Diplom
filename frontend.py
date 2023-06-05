# импорты
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id

from vk_api.keyboard import VkKeyboard, VkKeyboardColor

from config import community_token, access_token
from backend import VkTools

# отправка сообщений


class BotInterface():
    def __init__(self, community_token, access_token):
        self.vk = vk_api.VkApi(token=community_token)
        self.longpoll = VkLongPoll(self.vk)
        self.vk_tools = VkTools(access_token)
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

    def event_handler(self):
        for event in self.longpoll.listen():

            # Кнопки
            buttons = ['Привет', 'Поиск', 'Пока']
            button_colors = [VkKeyboardColor.PRIMARY, VkKeyboardColor.PRIMARY, VkKeyboardColor.PRIMARY]
            keyboard = self.chat_keyboard(buttons, button_colors)

            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                if event.text.lower() == 'привет':
                    '''Логика для получения данных о пользователе'''
                    self.params = self.vk_tools.get_profile_info(event.user_id)
                    if self.params is not None:  # Ошибка если инф. не получена
                        '''Запрос недостающих данных о пользователе'''
                        if not self.params['city']:
                            self.message_send(event.user_id, 'Для корректного поиска, пожалуйста, укажите в соей анкете ваш город проживания', keyboard=keyboard.get_keyboard())
                        elif not self.params['sex']:
                            self.message_send(event.user_id, 'Для корректного поиска, пожалуйста, укажите в соей анкете ваш пол', keyboard=keyboard.get_keyboard())
                        elif not self.params['year']:
                            self.message_send(event.user_id, 'Для корректного поиска, пожалуйста, укажите в соей анкете вашу дату рождения', keyboard=keyboard.get_keyboard())
                        elif not self.params['relation']:
                            self.message_send(event.user_id, 'Для корректного поиска, пожалуйста, укажите в соей анкете ваше семейное положение', keyboard=keyboard.get_keyboard())
                        else:
                            self.message_send(event.user_id, f'Привет, {self.params["name"]}!, нажми "Поиск", чтобы я нашел анкеты', keyboard=keyboard.get_keyboard())
                    else:
                        self.message_send(event.user_id, 'Ошибка получения данных', keyboard=keyboard.get_keyboard())
                elif event.text.lower() == 'поиск':
                    '''Логика для поиска анкет'''
                    self.message_send(
                        event.user_id, 'Начинаем поиск', keyboard=keyboard.get_keyboard())
                    if self.worksheets:
                        worksheet = self.worksheets.pop()
                        photos = self.vk_tools.get_photos(worksheet['id'])
                        photo_string = ''
                        for photo in photos:
                            photo_string += f'photo{photo["owner_id"]}_{photo["id"]},'
                    else:
                        self.worksheets = self.vk_tools.search_worksheet(self.params, self.offset)
                        worksheet = self.worksheets.pop()
                        '''првоерка анкеты в бд в соотвествие с event.user_id'''

                        photos = self.vk_tools.get_photos(worksheet['id'])
                        photo_string = ''
                        for photo in photos:
                            photo_string += f'photo{photo["owner_id"]}_{photo["id"]},'
                        self.offset += 50

                    self.message_send(
                        event.user_id,
                        f'Имя: {worksheet["name"]}. Страница: vk.com/id{worksheet["id"]}',
                        attachment=photo_string, keyboard=keyboard.get_keyboard()
                    )

                    'добавить анкету в бд в соотвествие с event.user_id'

                elif event.text.lower() == 'пока':
                    self.message_send(
                        event.user_id, 'До новых встреч', keyboard=keyboard.get_keyboard())
                else:
                    self.message_send(
                        event.user_id, 'Неизвестная команда', keyboard=keyboard.get_keyboard())


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
