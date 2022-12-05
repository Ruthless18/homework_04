"""
Домашнее задание №4
Асинхронная работа с сетью и бд

доработайте функцию main, по вызову которой будет выполняться полный цикл программы
(добавьте туда выполнение асинхронной функции async_main):
- создание таблиц (инициализация)
- загрузка пользователей и постов
    - загрузка пользователей и постов должна выполняться конкурентно (параллельно)
      при помощи asyncio.gather (https://docs.python.org/3/library/asyncio-task.html#running-tasks-concurrently)
- добавление пользователей и постов в базу данных
  (используйте полученные из запроса данные, передайте их в функцию для добавления в БД)
- закрытие соединения с БД
"""
import asyncio

from mod.jsonplaceholder_requests import USERS_DATA_URL, POSTS_DATA_URL, get_json

from mod.models import create_tables, create_users, create_posts



async def async_main():
    await create_tables()
    user_data, post_data = await asyncio.gather(
        get_json(USERS_DATA_URL),
        get_json(POSTS_DATA_URL),
    )
    await create_users(user_data)
    await create_posts(post_data)


def main():
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
