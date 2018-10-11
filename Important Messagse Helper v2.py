import vk_api
import random
from collections import defaultdict
import operator
from time import  sleep

# Авторизация
vk_session = vk_api.VkApi('логин от вк', 'пароль')
vk_session.auth()
vk = vk_session.get_api()
me = vk_session.token['user_id']

def make_msg_link(message):
    return f"https://vk.com/im?msgid={message['id']}&sel={message['peer_id']}"

peer = 2000000000 + 194 # Заменить 194 на Id беседы, в которую должны скидываться важные сообщения
skip_list = [] # Перечисление диалогов (id пользователей и групп), которые пропускать из обработки

# Получение всех важных
count = int(vk.messages.getImportantMessages(count=0)['messages']['count'])
msgs = []
offset = 0
while(True):
    print('.')
    temp = vk.messages.getImportantMessages(offset=offset, count=200)
    if len(temp['messages']['items']) == 0:
        break
    msgs.extend(temp['messages']['items'])
    offset = offset + 200

msgs_by_dialogs = defaultdict(list)

for m in msgs:
    msgs_by_dialogs[m['peer_id']].append(m)

vk.messages.send(peer_id=peer, message='Всего важных: ' + str(count) + '\nДиалогов: ' + str(len(msgs_by_dialogs)))

for s in skip_list:
    del msgs_by_dialogs[s]

dialogs_count = {key: len(val) for key,val in msgs_by_dialogs.items()}
dialogs_count = sorted(dialogs_count.items(), key=operator.itemgetter(1))[0:]
min_dialogs = dict(dialogs_count[0:5])
for peer_id in min_dialogs.keys():
    mm = msgs_by_dialogs[peer_id]
    #mm = mm[::-1]
    random.shuffle(mm)
    if len(msgs_by_dialogs[peer_id]) > 5:
        mm = mm[0:5]
    for m in mm:
        sleep(0.5)
        try:
            vk.messages.send(peer_id=peer, message=make_msg_link(m), forward_messages=m['id'])
        except:
            pass