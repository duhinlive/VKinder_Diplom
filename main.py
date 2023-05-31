from pprint import pprint
import vk_api
from vk_api.exceptions import ApiError

from config import access_token


#получкение данных о пользователе

class VKTools:
	def __init__(self, access_token):
		self.vkapi = vk_api.VkApi(token = access_token)


	def get_profile_info(self, user_id):

		try:
			info, = self.vkapi.metod('users.get',
						{'user_id': user_id,
						'fields': 'city, sex, bdate, relation'
						}
						)
		except ApiError as e:
			info = {}
			print(f'error = {e}')


		result = {'name': info['first_name'] + ' ' + info['last_name'],
			'sex': info['sex'],
			'city': info['city']['title'],
			'bdate': info['bdate']
			}
		return result


if __name__ == '__main__':
	user_id = 803689260
	tools = VkTools(access_token)
	params = tools.get_profile_info(user_id)



