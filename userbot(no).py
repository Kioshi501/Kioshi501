#pip install telethon

from telethon import TelegramClient
from telethon.sessions import StringSession

# Замените на ваши данные
API_ID = 1234567  # Ваш API ID
API_HASH = "YOUR_API_HASH"  # Ваш API HASH
SESSION_STRING = "YOUR_SESSION_STRING"  # Ваша строка сессии


async def main():
    async with TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH) as client:
        # Получаем информацию о пользователе
        me = await client.get_me()
        print(f"Имя пользователя: {me.first_name} {me.last_name}")

        # Отправляем сообщение в чат (замените на ID вашего чата)
        await client.send_message(7777777, "Привет из Hikka Telethon!") # Замените 7777777 на ID чата


import asyncio
asyncio.run(main())