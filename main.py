from pprint import pprint
import vk_api

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
		except _