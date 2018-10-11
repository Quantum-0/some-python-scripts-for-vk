from pip._internal import main
main(["install", "vk_api"])

chat_name = 'Test Chat 123'
vk_login, vk_pass = 'логин', 'пароль'

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType, VkChatEventType

import random
import os.path

def get_chat_id_or_create():
    global chat_id

    if os.path.isfile('ChatID.txt'):
        with open('ChatID.txt', 'r') as f:
            chat_id = int(f.readline())
            return chat_id
    else:
        chat_id = int(vk.messages.createChat(title=chat_name))
        with open('ChatID.txt','w') as f:
            f.write(str(chat_id))
        return chat_id

def regenerate_invite_link():
    global chat_id
    peer_id = 2000000000 + chat_id
    link = vk.messages.getInviteLink(peer_id=peer_id, reset=1)['link']
    return link

testing = {}
failed = []

def main():
    global vk
    global testing
	global failed
    vk_session = vk_api.VkApi(vk_login, vk_pass)

    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return

    longpoll = VkLongPoll(vk_session)
    vk = vk_session.get_api()

    get_chat_id_or_create()

    for event in longpoll.listen():
        if event.type == VkEventType.CHAT_UPDATE:
            if event.update_type == VkChatEventType.USER_JOINED:
                regenerate_invite_link()
        if event.type == VkEventType.MESSAGE_NEW and event.from_user:
            if event.text == 'ХОЧУ В КОНФУ':
                if event.user_id not in testing.keys():
                    a = random.randint(10, 100)
                    b = random.randint(10, 100)
                    testing[event.user_id] = a + b
                    vk.messages.send(user_id = event.user_id, message = f'Агааа, в конфу хочешь? Хорошо, я тебя пущу в конфу, но лишь с одним условием. Ты мне скажешь, сколько будет {a} + {b}')
                elif event.user_id not in failed:
                    vk.messages.send(user_id=event.user_id,
                                     message=f'Нет, ты ответил неверно, поэтому теперь я тебя не пущу')
			elif event.user_id in testing.keys():
				if event.text.isdigit():
					if int(event.text) != testing[event.user_id]:
						vk.messages.send(user_id = event.user_id, message = 'Неправильно, ты проиграл :с')
						failed.append(event.user_id)
						del testing[event.user_id]
					else:
						link = regenerate_invite_link()
						vk.messages.send(user_id = event.user_id, message = 'Молодец, держи ссылку: \n' + link)
						del testing[event.user_id]

if __name__ == '__main__':
    main()