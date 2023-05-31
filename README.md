# vk-wall-downloader
Скачивает все фото со стены человека, не качает сохраненные фотографии

## Использование
Установите все необходимые библиотеки:
- в cmd перейдите к папке где расположен скрипт
- введите pip install -r requirements.txt

Перед тем как использовать скрипт пройдитесь по пунктам ниже:
1. Создаете vk приложение - https://vk.com/editapp?act=create (вы должны быть зарегестрированны в VK)
2. Делаете зарос по ссылке ниже, вставив в строку id вашего приложения
https://oauth.vk.com/authorize?client_id=ID_ВАШЕГО_ПРИЛОЖЕНИЯ&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=photos&response_type=token&v=5.52
4. Из ответной строки поиска берете токен
- Вид ответной ссылки - https://oauth.vk.com/blank.html#access_token=vk1.a.EdQL_vPLxsbg4VNGvZJqh2ga-nvRUfvkNJSrH33x2s_7k672SVFxNQjnc1p4pktow-PYxJywQOMrZsZPfwy-mH6f0kTl7gQ5MAgHR1kxwkvr5Jr99NaYYRQuujbHd4R_dz4QczhGTs9yTaC-H6SVa0oxyoyauf5JRaDf8rX9BhmJZyJwkTfFzHcLHOsVh28E&expires_in=86400&user_id=123456789

Где:
- Токен = vk1.a.EdQL_vPLxsbg4VNGvZJqh2ga-nvRUfvkNJSrH33x2s_7k672SVFxNQjnc1p4pktow-PYxJywQOMrZsZPfwy-mH6f0kTl7gQ5MAgHR1kxwkvr5Jr99NaYYRQuujbHd4R_dz4QczhGTs9yTaC-H6SVa0oxyoyauf5JRaDf8rX9BhmJZyJwkTfFzHcLHOsVh28E
- Время действия токена - 86400 сек (можно изменить, гуглите сами)
- ID юзера(ваш) - 123456789

## Теперь получаем id у кого собираетесь собирать фото:
1. Нажимаем на любое фото и видим ссылку:
    https://vk.com/albums123123123?z=photo123123123_457244488%2Fphotos123123123
2. смотрим на photo123123123_457244488 id находиться между photo и _
3. id данного человека 123123123

# Вводим внури скрипта id и VK_TOKEN и запускаем скрипт, готово!
