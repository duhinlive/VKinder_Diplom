# импорты
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id

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

    def message_send(self, user_id, message, attachment=None):
        self.vk.method('messages.send',
                       {'user_id': user_id,
                        'message': message,
                        'attachment': attachment,
                        'random_id': get_random_id()}
                       )

# обработка событий / получение сообщений

    def event_handler(self):
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                if event.text.lower() == 'привет':
                    '''Логика для получения данных о пользователе'''
                    self.params = self.vk_tools.get_profile_info(event.user_id)
                    self.message_send(
                        event.user_id, f'Привет друг, {self.params["name"]}')
                elif event.text.lower() == 'поиск':
                    '''Логика для поиска анкет'''
                    self.message_send(
                        event.user_id, 'Начинаем поиск')
                    if self.worksheets:
                        worksheet = self.worksheets.pop()
                        photos = self.vk_tools.get_photos(worksheet['id'])
                        photo_string = ''
                        for photo in photos:
                            photo_string += f'photo{photo["owner_id"]}_{photo["id"]},'
                    else:
                        self.worksheets = self.vk_tools.search_worksheet(
                            self.params, self.offset)

                        worksheet = self.worksheets.pop()
                        'првоерка анкеты в бд в соотвествие с event.user_id'

                        photos = self.vk_tools.get_photos(worksheet['id'])
                        photo_string = ''
                        for photo in photos:
                            photo_string += f'photo{photo["owner_id"]}_{photo["id"]},'
                        self.offset += 10

                    self.message_send(
                        event.user_id,
                        f'имя: {worksheet["name"]} ссылка: vk.com/{worksheet["id"]}',
                        attachment=photo_string
                    )

                    'добавить анкету в бд в соотвествие с event.user_id'

                elif event.text.lower() == 'пока':
                    self.message_send(
                        event.user_id, 'До новых встреч')
                else:
                    self.message_send(
                        event.user_id, 'Неизвестная команда')


if __name__ == '__main__':
    bot_interface = BotInterface(community_token, access_token)
    bot_interface.event_handler()
