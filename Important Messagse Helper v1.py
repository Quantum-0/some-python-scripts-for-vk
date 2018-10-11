#from pip._internal import main
#main(["install", "vk_api"])

import vk_api
import random
from datetime import  datetime

# Авторизация
vk_session = vk_api.VkApi('логин от вк', 'пароль от вк')
vk_session.auth()
vk = vk_session.get_api()
me = vk_session.token['user_id']
peer = 2000000000 + 194
msglink = 'https://vk.com/im?msgid={}&sel={}'
info = '== Рандомное важное сообщение ==\n\nВсего важных сообщений: {}\nПересланное сообщение: #{}\n\n'

# Получение количества
count = int(vk.messages.getImportantMessages(count=0)['messages']['count'])
for ii in [1,2,3]:
    # Получение рандомного сообщения из важных
    i = random.randint(0, count-1)
    randmsg = vk.messages.getImportantMessages(count=1, offset=i)['messages']['items'][0]
    # Отправка ссылки и пересланного сообщения
    vk.messages.send(peer_id = peer, message = info.format(count,i) + msglink.format(randmsg['id'], randmsg['peer_id']), forward_messages = randmsg['id'])