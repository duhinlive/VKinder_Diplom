# VKinder_Diplom
Бот для поиска пары в ВК

https://vk.com/id803689260 Андрей Духин
https://vk.com/club220790423 VKinderGroup


Бот ищет людей, подходящих под условия, на основании информации о пользователе из VK: Возраст, 
пол, город.

У тех людей, которые подошли по требованиям получаем топ-3 популярных фотографии профиля в чат 
вместе со ссылкой на найденного человека. Популярность определяется по количеству лайков и 
комментариев.

Если информации о пользователе недостаточно, то после нажатия кнопки Привет - запрашивается, 
если отсутствует, пол, дата рождения, город, семйное положение.

Код программы удовлетворяет PEP8. 
Токены находятся в файле config.py 
Программа декомпозирована на функции/классы/модули/пакеты. 
ID найденных пользователей и ID анкет записываются в БД в таблицу Viwed. 
Люди не повторяются при повторном поиске, так как анкеты проходят проверку на уже просмотренные.