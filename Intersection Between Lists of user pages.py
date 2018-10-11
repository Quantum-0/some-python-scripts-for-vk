# Intersection of sets of vk links for Дым

# Некоторые настройки

vk_login, vk_pass = 'Логин от Вк', 'Пароль от Вк'
output_vk_msg = True # Вывод в виде сообщения вк
output_file = True # Вывод в виде файла

# Подключение вк. Если интерпретатор ругается на эту строку, нужно выполнить в консоли следующее: pip3 install vk_api

import vk_api

# Авторизация
vk_session = vk_api.VkApi(vk_login, vk_pass)
vk_session.auth()
vk = vk_session.get_api()
me = vk_session.token['user_id']

# Функция, преобразования текстовой ссылки в id (число)
def link_to_id(link):
    link.strip() # Убираем имеющиеся пробелы в начале и в конце строки, есл те имеются
    link = link.replace('https://', '').replace('http://', '') # Убираем протокол из url, если он имеется
    link = link.replace('www.', '') # Убираем www, если оно имеется
    link = link.replace('vk.com/', '') # Убираем vk.com/, если оно есть
    link = link.split('/')[0] # Разделяем строку по символам "/" и берём первый кусок
    if link == '': # Если ссылка после этих всех преобразований превратилась в пустую строку - значит ссылка была кривая
        raise Exception('Неудалось распарсить ссылку на пользователя')
    try: # Если же всё прошло удачно - пытаемся запросить у вк данные об этом пользователе и вытащить из них ID
        return int(vk.users.get(user_ids = link)[0]['id'])
    except vk_api.ApiError: # Если VK API выдал ошибку, значит пользователь не существует, т.е. например изменил ссылку на свою страницу
        return None

# Функция, вытаскивающая из файла список ссылок
def load_links_list_from_file(fname):
    with open(fname, "r") as links_file:
        return links_file.readlines()

# Функция, превращающая список ссылок в множество айдишников
def links_list_to_ids_set(links):
    return set(filter(None, map(link_to_id, links)))

# Функция, записывающая список/множество строк в файл (подходит для записи списка ссылок, айдишников и т.п.)
def save_ids_set_to_file(fname, ids):
    with open(fname, 'w') as f:
        for item in ids:
            f.write("%s\n" % str(item))

# Пересечение множеств
def intersect_two_sets(set1, set2):
    return set1 & set2

# Преобразование списка айдишников в список ссылок
def ids_to_links(ids):
    return ['https://vk.com/id' + str(x) for x in ids]

# Отправка результата себе вк
def send_message_to_me(msg):
    vk.messages.send(peer_id=me, message='== Результат выполнения скрипта ==\n\n' + msg)

# Преобразование списка или множества в сообщение
def list_to_msg(list):
    return '\n'.join(list)


# Ну и далее сама программа

list1 = load_links_list_from_file('D:\\list1.txt')
list2 = load_links_list_from_file('D:\\list2.txt')
set1 = links_list_to_ids_set(list1)
set2 = links_list_to_ids_set(list2)
intersection = intersect_two_sets(set1, set2)
intersected_links = ids_to_links(intersection)
if output_vk_msg:
    msg = list_to_msg(intersected_links)
    send_message_to_me(msg)
if output_file:
    save_ids_set_to_file('D:\\output.txt', intersection)