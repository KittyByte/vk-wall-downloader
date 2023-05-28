import aiofiles
import aiohttp
import asyncio
from aiohttp_retry import RetryClient

import json
import requests
import time
import os


VK_TOKEN = ''
VK_USER_ID = 123123123  # id человека у кого берете фото
counter = 0  # просто счетчик

if not os.path.exists('images'):
    os.mkdir('images')


def get_photo_data(offset=1, count=200) -> json.loads:
    """
    offset - значение озночающая сдвиг, пример: у вас 1300 фото, мах запрос 200, ставя offset на 1 вы получаете данные с 201 по 400, offset 2 с 401 по 600 и тд.
    count - количество фото получаемое за раз мах 200
    """
    api = requests.get('https://api.vk.com/method/photos.getAll', params={
        'owner_id': VK_USER_ID,
        'access_token': VK_TOKEN,
        'offset': offset,
        'count': count,
        'photo_sizes': 0,
        'v': 5.103
    })
    return json.loads(api.text)


async def check_name(filename) -> str:
    """ проверка на содержание символов которые винда запрещает для имени файла при его записи """
    bad = ['/', '\\', ':', '?', '"', '*', '<', '>', '|']
    for bad_sim in bad:
        if bad_sim in filename:
            filename = filename.replace(str(bad_sim), '')

    return filename


async def get_photo(url, client_retry):
    global counter
    filename = await check_name(url.split('/')[-1])
    async with aiofiles.open(f'images/{filename}.jpg', 'wb') as f:  # создаем файл и асинхронно работаем с ним
        async with client_retry.get(url) as responce:  # делаем запрос на файл фото
            async for chunck in responce.content.iter_chunked(5120):  # по кусочкам записывает файл
                await f.write(chunck)
    counter += 1
    print(f'\r[+] Файлов {counter} записано', end='')


async def gather_tasks(list_urls, client_retry):
    """ т.к у VK ограничение по единовременному скачиванию файлов, сделал функцию для загрузок по 200 фото за раз"""
    tasks = []
    for url in list_urls:
        task = asyncio.create_task(get_photo(url, client_retry))
        tasks.append(task)

    await asyncio.gather(*tasks)


async def save_all_photos(list_of_list_urls):
    async with aiohttp.ClientSession() as session:
        client_retry = RetryClient(session)
        for list_urls in list_of_list_urls:
            await gather_tasks(list_urls, client_retry)


async def get_photo_urls():
    photos_urls = []

    data = get_photo_data()
    try:
        count_photo = data['response']['count']
    except:
        print(data)
        print('[+] Ошибка в обработке ответа, скорее всего время вашего токена истекло или вы вставили неправильный токен')
        exit()

    print('[+] Всего фото -', count_photo)

    i = 0
    count = 200  # количество файлов которые мы получим за раз, мах 200
    while i <= count_photo:
        data = get_photo_data(offset=i, count=count)
        for files in data['response']['items']:
            file_url = files['sizes'][-1]['url']
            photos_urls.append(file_url)
        i += count

    print('[+] Получение всех ссылок -', len(photos_urls))

    chunk_size = count
    # создаем списки по количеству файлов которые мы получаем, мах 200 иначе появится ошибка
    list_of_list_urls = [photos_urls[i:chunk_size + i] for i in range(0, len(photos_urls), chunk_size)]

    await save_all_photos(list_of_list_urls)


async def main():
    await get_photo_urls()


if __name__ == '__main__':
    now = time.perf_counter()
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
    print(f'\n\n[+] Затрачено времени: {time.perf_counter() - now:.2f} сек')
