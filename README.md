# Some Python Scripts For VK
Несколько моих полезных (и не очень) скриптов для ВК

# Зависимости
Все скрипты требуют для запуска python3 и библиотеку vk_api

# Intersection Between Lists of user pages.py
Данный скрипт был написан по просьбе.

Цель скрипта - взять 2 списка ссылок в виде txt файлов, преобразовать их в списки с идентификаторами пользователей и затем найти пересечения, т.е. выдать список пользователей, ссылки на которых присутствуют в обоих файлах, в том числе учитывая, что ссылки могут иметь разный вид (одна - screen_name страницы, другая - idXXXXXXX)

# Important Messagse Helper v1.py
Данный скрипт был написан для себя.

В каком-то момент я столкнулся с проблемой, что у меня слишком много сообщений ВК, помеченных как "важные" (около 2 - 2,5 тысяч). Многие из них на данный момент уже не актуальны, но, к сожалению, с помощью сайта и мобильного приложения я могу просмотрить их лишь в хронологическом порядке начиная с последних. Несколько десятков последних актуальны, а те, что находятся дальше - сложно достяжимы. Притом один неверный клик - и список нужно листать заного. Для решения этой проблемы был написан данный скрипт, который находит все важные сообщения и присылает случайное из них, таким образом помогая перебрать старые важные соощения и разобраться в них.

# Important Messagse Helper v2.py
Данный скрипт представляет из себя улучшенную версию Important Messagse Helper v1.py

Он разбивает все важные сообщения по диалогам, сортирует диалоги по количеству важных сообщений и первым делом предлагает разобрать те диалоги, где минимальное, но отличное от нуля количество важных сообщений.

После очистки важных сообщений с данным скриптом удалось намного быстрее чем вручную удалить несколько сотен важных сообщений в течении пары дней с устаревшими туду-шниками, туториалами по технологиям, которые я уже изучил, либо перестали быть актуальны для меня и прочим бесполезным мусором, а так же найти некоторую важную информацию, утерянную в этой куче важных соощений.

# Wall Cleaner.py
Данный скрипт был создан, чтобы очистить стену Вк от различных мемов и репостов с тупыми шутками, при этом чтобы оставить собственные посты, что-то важное, сохранить посты по фильтрам (например, имеющие комменты или лайки), а так же различные розыгрыши и лотереи

# Groups Compare.py
Данный скрипт сохраняет список групп, в которых состоит пользователь, и при последующих запусках сообщает о том, из каких групп пользователь вышел (либо был исключён), а так же, в какие группы пользователь вступил. Скрипт был написан по той причине, что я подписан на несколько групп художников, которые имеют противную привычку - периодически удалять из группы неактивных участников. Данный скрипт позволяет увидеть, кто же удалил пользователя из группы, чтобы затем вступить в неё снова ;)

# gc_v2.py
Обновлённый Groups Compare.py
Теперь он умеет сообщать об изменении названия группы, а также смены типа между открытой группой, закрытой и частной

# Auto Chat Inviter.py
Попытка создать скрипт для бота, который приглашает в беседу с некоторым предварительным тестированием пользователя. Бот задаёт пользователю, желающему вступить в беседу, вопрос, при верном ответе на который бот предоставляет пользователю ссылку на вступление, при неправильном ответе бот добавляет пользователя в список проваливших тест и больше не пользовает ему вступить в беседу. Каждый раз при вступлении нового пользователя в беседу бот генерирует новую ссылку, обнуляя старую, таким образом предотвращая вступление в беседу несколькими людьми по одной ссылке

# ConversationsCleaner.py
Скрипт, написанный опять же по просьбе, помогающий разобраться в куче диалогов. Работает по принципу, аналогичному Important Messagse Helper, т.е. присылает ссылку на случайный диалог пользователя. Но кроме этого, данный скрипт получает событие о том, что пользователь открыл диалог, прочитал его либо ответил и присылает ссылку на следующий.
