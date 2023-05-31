from pprint import pprint
import vk_api
from vk_api.exceptions import ApiError

from config import access_token


#получение данных о пользователе

class VKTools:
	def __init__(self, access_token):
		self.vkapi = vk_api.VkApi(token = access_token)


	def get_profile_info(self, user_id):

		try:
			info, = self.vkapi.metod('users.get',
						{'user_id': user_id,
						'fields': 'city, sex, bdate, relation'
						}
						) #если дата рождения или город, пол is None, то запрашивать у пользлвателя,
		# обрабатывая result. Проверить его на поля, которые в нем None и те поля которые None отправит пользователю запрос
		except ApiError as e:
			info = {}
			print(f'error = {e}')

		result = {'name': (info['first_name'] + ' ' + info['last_name'])
					if 'first_name' in info	and 'last_name' in info else None,
			'sex': info.get('sex'),
			'city': info.get('city')['title'] if info.get('city') is not None else None,
			'bdate': info.get('bdate')
			}
		return result


if __name__ == '__main__':
	user_id = 803689260
	tools = VkTools(access_token)
	params = tools.get_profile_info(user_id)




