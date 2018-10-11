#from pip._internal import main
#main(["install", "vk_api"])

import vk_api
from datetime import datetime

# Авторизация
vk_session = vk_api.VkApi('логин от вк', 'пароль')
vk_session.auth()
vk = vk_session.get_api()
me = vk_session.token['user_id']
fname = 'Groups List ' + str(me) + '.txt'

msg = '== Проверка изменений в списке групп ==\n\n'

# Получение списка групп (на данный момент)
groups_list = []
offset = 0
while (True):
    temp = vk.groups.get(offset=offset, count=1000, extended=True)
    if len(temp['items']) == 0:
        break
    groups_list.extend(temp['items'])
    offset = offset + 1000

groups = [{'id': g['id'], 'name': g['name'], 'type': g['type'], 'is_closed': g['is_closed'], 'is_admin': g['is_admin'] if 'is_admin' in g else None, 'admin_level': g['admin_level'] if 'admin_level' in g else None} for g in groups_list]
groups_by_id = {g['id']: {'name': g['name'], 'type': g['type'], 'is_closed': g['is_closed'], 'is_admin': g['is_admin'] if 'is_admin' in g else None, 'admin_level': g['admin_level']} for g in groups}
groups_ids = [g['id'] for g in groups]


# Получение списка групп из файла
import os.path
if os.path.isfile(fname):
    old_groups = []
    with open(fname, 'r') as fp:
        dt = fp.readline().strip()
        #print(dt)
        dt = datetime.strptime(dt, '%b %d %Y %I:%M%p')
        for line in fp:
            old_groups.append(int(line.strip()))

    msg += 'Дата последнего обновления: ' + dt.strftime('%d %b %Y %I:%M%p') + '\n'

    # Сравнение
    old = set(old_groups)
    new = set(groups_ids)

    enter = new - old
    leave = old - new

    msg += f'Подписок на новые группы: {len(enter)}\nОтписок от старых групп: {len(leave)}\n\n'

    if len(leave) > 0:

        finded = vk.groups.getById(group_ids=','.join([str(l) for l in leave]))
        groups_finded = [{'id': g['id'], 'name': g['name'], 'type': g['type'], 'is_closed': g['is_closed'],
                   'is_admin': g['is_admin'] if 'is_admin' in g else None,
                   'admin_level': g['admin_level'] if 'admin_level' in g else None} for g in finded]
        groups_by_id_new = {g['id']: {'name': g['name'], 'type': g['type'], 'is_closed': g['is_closed'],
                                  'is_admin': g['is_admin'] if 'is_admin' in g else None,
                                  'admin_level': g['admin_level']} for g in groups_finded}
        groups_by_id.update(groups_by_id_new)

        print('Покинуты группы:')
        msg += 'Покинуты:\n'
        for i,g in enumerate(leave):
            print('https://vk.com/club' + str(g) + '\t\t' + str(groups_by_id[g]))
            msg += '[club' + str(g) + '|' + groups_by_id[g]['name'] + ']\n'
    if len(enter) > 0:
        print('Новые группы:')
        msg += '\nНовые:\n'
        for g in enter:
            print('https://vk.com/club' + str(g) + '\t\t' + str(groups_by_id[g]))
            msg += '[club' + str(g) + '|' + groups_by_id[g]['name'] + ']\n'
    if len(leave) == 0 and len(enter) == 0:
        print('За данный период изменения не обнаружены')
        msg += 'За данный период изменения не обнаружены\n'
    print('Дата последнего обновления:')
    print(dt)
else:
    print('Сохранённый ранее список групп отсутствует')
    msg += 'Сохранённый ранее список групп отсутствует.\n Список будет сгенерирован на текущую дату, дальнейшие изменения будут отслеживаться от текущего момента'

# Сохранение
with open(fname, 'w') as fp:
    fp.write(datetime.now().strftime('%b %d %Y %I:%M%p') + '\n')
    for gid in groups_ids:
        fp.write("%i\n" % gid)

# Отправка отчёта
vk.messages.send(user_id = me, message = msg)