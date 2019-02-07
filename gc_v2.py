# Groups Comparer v2

import vk_api
from datetime import datetime
import json
import platform, os
import random

TOKEN = 'Insert your token here'
ME = 0000000
if platform.system() == 'Windows':
    FILE = './groups' + str(ME) + '.json'
else:
    FILE = '/home/groups/' + str(ME) + '.json'

'''
Dict/Json file format:
{
[
{
    id: ...
    name: ...
    is_closed: 0 - открытая, 1 - закрытая, 2 - частная
}
]
}
'''

vk_session = vk_api.VkApi(token=TOKEN)
vk = vk_session.get_api()

def load_groups():
    groups_list = []
    offset = 0
    while (True):
        temp = vk.groups.get(offset=offset, count=1000, extended=True)
        if len(temp['items']) == 0:
            break
        groups_list.extend(temp['items'])
        offset = offset + 1000
    return [{'id': g['id'], 'name': g['name'], 'type': g['type'], 'is_closed': g['is_closed'],
             'is_admin': g['is_admin'] if 'is_admin' in g else None,
             'admin_level': g['admin_level'] if 'admin_level' in g else None} for g in groups_list]

def format_groups(groups_list):
    return [{'id': g['id'], 'name': g['name'], 'is_closed': g['is_closed']} for g in groups_list]

def save_to_file(groups_list):
    with open(FILE, 'w') as f:
        json.dump(groups_list, f, indent=2)

# Returns new_groups and leaved_groups
def compare_two_lists(before, after):
    if len(before) == 0 and len(after) > 50:
        return [], []
    before_ids = set([g['id'] for g in before])
    after_ids = set([g['id'] for g in after])
    enter_ids = after_ids - before_ids
    leave_ids = before_ids - after_ids
    enter = [g for g in after if g['id'] in enter_ids]
    leave = [g for g in before if g['id'] in leave_ids]
    return enter, leave

def get_by_id(groups_list, id):
    res = [g for g in groups_list if g['id'] == id]
    if len(res) == 1:
        return res[0]
    else:
        return None

def get_name_of_more_opened_group(gl1, gl2, id):
    g1 = get_by_id(gl1, id)
    g2 = get_by_id(gl2, id)
    if g1['is_closed'] < g2['is_closed']:
        return g1['name']
    else:
        return g2['name']

# Returns (id, old_name, new_name) list
def compare_names(before, after):
    before_ids = set([g['id'] for g in before])
    after_ids = set([g['id'] for g in after])
    common_ids = before_ids & after_ids
    changes = [{'id': id, 'old_name': get_by_id(before, id)['name'], 'new_name': get_by_id(after, id)['name']} for id in common_ids if  get_by_id(before, id)['name'] != get_by_id(after, id)['name']]
    return changes

# Returns (id, before, after) list
def compare_closeness(before, after):
    before_ids = set([g['id'] for g in before])
    after_ids = set([g['id'] for g in after])
    common_ids = before_ids & after_ids
    changes = [{'id': id, 'before': get_by_id(before, id)['is_closed'], 'after': get_by_id(after, id)['is_closed'], 'name': get_name_of_more_opened_group(before, after, id)} for id in common_ids if get_by_id(before, id)['is_closed'] != get_by_id(after, id)['is_closed']]
    return changes

def load_from_file():
    if os.path.isfile(FILE):
        with open(FILE, 'r') as f:
            return json.load(f)
    else:
        return []

def generate_and_send_report(old, new):
    msg = "== Groups Comparer v2 ==\n\n"
    entered, leaved = compare_two_lists(old, new)
    name_changed = compare_names(old, new)
    closeness_changed = compare_closeness(old, new)
    closeness_text = ['открытой', 'закрытой', 'частной']
    if len(entered) > 0:
        msg += 'Новые группы:\n'
        msg += '\n'.join(['> [club' + str(g['id']) + '|' + g['name'] + ']' for g in entered])
        msg += '\n'
    if len(leaved) > 0:
        msg += 'Покинутые группы:\n'
        msg += '\n'.join(['> [club' + str(g['id']) + '|' + g['name'] + ']' for g in leaved])
        msg += '\n'
    if len(name_changed) > 0:
        msg += 'Смена названий:\n'
        msg += '\n'.join(['> Сообщество ' + g['old_name'] + ' сменило название на [club' + str(g['id']) + '|' + g['new_name'] + ']' for g in name_changed])
        msg += '\n'
    if len(closeness_changed) > 0:
        msg += 'Изменение приватности:\n'
        msg += '\n'.join(['> Группа [club' + str(g['id']) + '|' + g['name'] + '] стала ' + closeness_text[g['after']] for g in closeness_changed])
    if len(entered) + len(leaved) + len(name_changed) + len(closeness_changed) == 0:
        msg += 'За прошедший день изменений не обнаружено'
    vk.messages.send(user_id=ME, message=msg, random_id=random.randint(0,9999999))


groups_old = load_from_file()
groups_new = format_groups(load_groups())
save_to_file(groups_new)
generate_and_send_report(groups_old, groups_new)