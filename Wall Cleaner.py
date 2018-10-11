from pip._internal import main
main(["install", "vk_api"])

import vk_api
from datetime import  datetime, timezone
from vk_api import VkTools

def print_posts(posts):
    for p in posts:
        print(f'- https://vk.com/wall{p["owner_id"]}_{p["id"]}')

# Авторизация
vk_session = vk_api.VkApi('логин', 'пароль')
vk_session.auth()
vk = vk_session.get_api()

# Скачивание
temp = vk.wall.get(count=1, filter='owner')
count = temp['count']
print(f'Найдено {count} постов. Загрузка всех постов..')
tools = VkTools(vk_session)
posts = tools.get_all('wall.get', 100, {'filter': 'owner'})['items']
print('Загрузка завершена')

# Фильтрация
def is_lottery(post, threshold = 7):
    scores = {
        'лот': 7,
        'лотере': 10,
        'розыгрыш': 8,
        'подписк': 5,
        'репост': 6,
        'победител': 9,
        'приз': 2,
        'место': 1
    }
    score = 0
    if 'copy_history' in post:
        text = post['copy_history'][0]['text'].lower()
        for word in scores.keys():
            if word in text:
                score += scores[word]
    return score >= threshold


posts_with_text = list(filter(lambda x: x['text'] != '', posts))
count_with_text = len(posts_with_text)
posts_own = list(filter(lambda x: 'copy_history' not in x, posts))
count_reposts = count - len(posts_own)
lottery_posts = list(filter(is_lottery, posts))
count_lottery = len(lottery_posts)
now = datetime.now()
last_week_posts = list(filter(lambda x: (now - datetime.fromtimestamp(x['date'])).days < 7, posts))
last_week_count = len(last_week_posts)
posts_with_comments = list(filter(lambda x: x['comments']['count'] > 0, posts))
posts_with_likes = list(filter(lambda x: x['likes']['count'] > 0, posts))
count_commented = len(posts_with_comments)
count_liked = len(posts_with_likes)
posts_from_friends = list(filter(lambda x: x['owner_id'] != x['from_id'], posts))
count_from_friends = len(posts_from_friends)

print(f'Всего постов: {count}\nС текстом: {count_with_text}\nРепосты: {count_reposts}\nСобственные: {count - count_reposts}\nПредположительно лотереи и розыгрыши: {count_lottery}\nС комментами: {count_commented}\nС лайками: {count_liked}\nЗа последнюю неделю: {last_week_count}\nПостов от друзей: {count_from_friends}')

print('Не репосты:')
print_posts(posts_own)
print('С букафками:')
print_posts(posts_with_text)
print('Лотереи и розыгрыши:')
print_posts(lottery_posts)
print('Прокоментированые посты:')
print_posts(posts_with_comments)


# Фильтрация для удаления
save_own_posts = set((p['id'], p['owner_id']) for p in posts_own)
save_text_posts = set((p['id'], p['owner_id']) for p in posts_with_text)
save_lottery_posts = set((p['id'], p['owner_id']) for p in lottery_posts)
save_last_week_posts = set((p['id'], p['owner_id']) for p in last_week_posts)
save_commented_posts = set((p['id'], p['owner_id']) for p in posts_with_comments)
save_liked_posts = set((p['id'], p['owner_id']) for p in posts_with_likes)
save_from_friends = set((p['id'], p['owner_id']) for p in posts_from_friends)

save_posts = save_own_posts | save_text_posts | save_lottery_posts | save_last_week_posts | save_commented_posts | save_from_friends # | save_liked_posts
posts_to_delete = set((p['id'], p['owner_id']) for p in posts) - save_posts
count_to_delete = len(posts_to_delete)

print(f'Удаление {count_to_delete} постов..')
print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')

# Удаление !!!!!!!!!!!!!!!!!!!!!!!!!!!1
for p in posts_to_delete:
    print(f'Удаление поста https://vk.com/wall{p[1]}_{p[0]}')
    vk.wall.delete(owner_id = p[1], post_id = p[0])
print('Удаление завершено успешно!')
vk.wall.post(message = 'Стена почищена скриптом Тш\nМур <3')