from pip._internal import main
main(["install", "vk_api"])

import vk_api, random
from vk_api import VkTools
from vk_api.longpoll import VkLongPoll, VkEventType
import threading

dialog_types_dict = {
    'chat': 'Конфа',
    'user': 'Пользователь',
    'group': 'Диалог с сообществом'
}
cannot_write_reasons = {
    18: 'Пользователь заблокирован или удалён',
    900: 'ЧС',
    902: 'Закрыта личка',
    915: 'В сообществе отключены сообщения',
    916: 'В сообществе заблокированы сообщения',
    203: 'Нет доступа к сообществу'
}
commands_help = [
    'HELP / ПОМОЩЬ / СПРАВКА - Справка по работе скрипта',
    'РАНДОМНЫЙ / РАНДОМ / RANDOM / RND - Рандомный непрочитанный диалог',
    'ПЕРВЫЙ / ПЕРВ / FIRST - Первый непрочитанный диалог',
    'ПОСЛЕДНИЙ / ПОСЛ / LAST - Последний непрочитанный диалог',
    'ПОСЛ60 / LAST60 - Рандомный диалог из последних 60-ти',
    'СКИДЫВАТЬ РАНДОМНЫЕ / RANDOM LOOP - Непрерывно скидывать непрочитанные диалоги',
    'STOP LOOP - Остановить цикл скидывания непрочитанных рандомных диалогов',
    'ВЫХОД / EXIT - Завершение работы'
]

def send_message_to_me_from_group(text):
    vk_group.messages.send(user_id=my_id, message='== Помощник в обработке непрочитанных диалогов ==\n\n' + text)

def auth():
    global vk
    global vk_group
    global vk_tools
    global my_id
    global vk_longpoll
    global vk_group_longpoll
    global vk_group_id

    vk_login, vk_pass = ('логин', 'пароль')
    vk_session = vk_api.VkApi(vk_login, vk_pass)
    vk_session.auth()
    vk = vk_session.get_api()
    vk_tools = VkTools(vk_session)
    vk_group_session = vk_api.VkApi(
        token='токен группы, выступающей в качестве бота, помогающего разбирать диалоги')
    vk_group = vk_group_session.get_api()
    my_id = int(vk_session.token['user_id'])
    vk_longpoll = VkLongPoll(vk_session)
    vk_longpoll = VkLongPoll(vk_session)
    vk_group_longpoll = VkLongPoll(vk_group_session)
    vk_group_id = -00000000 # ID группы

def get_unreaded_dialogs():
    return vk_tools.get_all('messages.getConversations', 100, {'filter': 'unread'})['items']

def generate_message_about_random_dialog():
    unreaded_dialogs = get_unreaded_dialogs()
    count = len(unreaded_dialogs)
    rnd = random.choice(unreaded_dialogs)
    return generate_message_about_random_dialog(rnd, count)

def generate_message_about_last_dialog():
    unreaded_dialogs = get_unreaded_dialogs()
    count = len(unreaded_dialogs)
    last = unreaded_dialogs[-1]
    return generate_message_about_random_dialog(last, count)

def generate_message_about_last60_dialog():
    unreaded_dialogs = get_unreaded_dialogs()
    count = len(unreaded_dialogs)
    last = random.choice(unreaded_dialogs[-60: -1])
    return generate_message_about_random_dialog(last, count)

def generate_message_about_first_dialog():
    unreaded_dialogs = get_unreaded_dialogs()
    count = len(unreaded_dialogs)
    first = unreaded_dialogs[0]
    return generate_message_about_random_dialog(first, count)

def generate_message_about_random_dialog(dialog, dialogs_count):
    global current_working_dialog

    dialog_type = dialog['conversation']['peer']['type']
    current_working_dialog = dialog['conversation']['peer']['id']
    dialog_link = 'https://vk.com/im?sel=' + str(current_working_dialog)
    can_write = dialog['conversation']['can_write']
    unread_messages = dialog['conversation']['unread_count']

    msg = 'Всего непрочитанных диалогов: ' + str(dialogs_count) + '\n'
    msg += 'Рандомный диалог: ' + dialog_link + '\n'
    msg += 'Тип диалога: ' + dialog_types_dict[dialog_type] + '\n'
    msg += 'Количество непрочитанных сообщений в диалоге: ' + str(unread_messages) + '\n'

    if dialog_type == 'user':
        usr = vk.users.get(user_ids=dialog['conversation']['peer']['id'])[0]
        usr = usr['first_name'] + ' ' + usr['last_name']
        msg += 'Собеседник: ' + usr + '\n'
    elif dialog_type == 'group':
        group = vk.groups.getById(group_ids=dialog['conversation']['peer']['id'])[0]
        group = group['name']
        msg += 'Группа: ' + group + '\n'

    if not can_write['allowed']:
        if can_write['reason'] in cannot_write_reasons.keys():
            msg += 'Ответить невозможно, причина: ' + cannot_write_reasons[can_write['reason']] + '\n'
        else:
            msg += 'Ответить невозможно по неизвестной причине\n\n'
    return msg




random_loop = False
last_msg_id = None
remove_message_next_iteration_flag = False
def group_longpoll():
    global my_id
    global random_loop
    global last_msg_id
    global remove_message_next_iteration_flag
    for event in vk_group_longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.from_user and event.user_id == my_id:
            text = event.text.lower()
            if text == 'help' or text == 'справка' or text == 'помощь':
                send_message_to_me_from_group('Список доступных команд:\n' + '\n'.join(commands_help))
            if text == 'рандомный' or text == 'рандом' or text == 'random' or text == 'rnd':
                send_message_to_me_from_group(generate_message_about_random_dialog())
            if text == 'первый' or text == 'перв' or text == 'first':
                send_message_to_me_from_group(generate_message_about_first_dialog())
            if text == 'последний' or text == 'посл' or text == 'last':
                send_message_to_me_from_group(generate_message_about_last_dialog())
            if text == 'посл60' or text == 'last60':
                send_message_to_me_from_group(generate_message_about_last60_dialog())
            if text == 'скидывать рандомные' or text == 'random loop':
                remove_message_next_iteration_flag = True
                send_message_to_me_from_group(generate_message_about_last60_dialog())
                random_loop = True
            if text == 'stop loop':
                random_loop = False
                remove_message_next_iteration_flag = False
                send_message_to_me_from_group('Цикл остановлен')
            if text == 'выход' or text == 'exit':
                exit(0)








auth()
send_message_to_me_from_group('Скрипт запущен. Напишите HELP/СПРАВКА/ПОМОЩЬ для справки.')
current_working_dialog = 1
thr = threading.Thread(target=group_longpoll)
thr.start()
last_msg_id = None
for event in vk_longpoll.listen():
    if event.type == VkEventType.READ_ALL_INCOMING_MESSAGES and event.peer_id == current_working_dialog:
        if random_loop:
            remove_message_next_iteration_flag = True
            last_msg_id = send_message_to_me_from_group('Yay!\nМолодец!\n\n' + generate_message_about_last60_dialog())
        else:
            send_message_to_me_from_group('Минус один х)\nТы молодец :з')
    if remove_message_next_iteration_flag and event.type == VkEventType.MESSAGE_NEW and event.peer_id == vk_group_id:
        remove_message_next_iteration_flag = False
        vk.messages.markAsRead(peer_id=vk_group_id, start_message_id=last_msg_id)
        last_msg_id = event.message_id