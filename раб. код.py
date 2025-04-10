import requests
import time
import asyncio
from telegram import InputMediaPhoto
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes



VK_ACCESS_TOKEN = "vk1.a.1Rf-YIOJoRjA-9asYdqpWnLiXMHaLOBPGKB9K2fyTXOaLHQWE_XqqMtHp8gaTp3wn1p7S5ZkqpSIXmx6L9g6JLjaca8NQJqHqcyN9TlJ90-deMPk_UI3DGu6oYTO2GLhf_0e_jb_tsXNuh8bzUBdwEQCRX49h07gRpqRQ3Qvcqc0wgMljM9BhAnyAT_42fFdVSVmI1ZZM0HMIiBuTzQM7w"
TELEGRAM_BOT_TOKEN = "8067916773:AAGH4WdeAOkyDmmrjnzcAFBnlViE1Lw7GBs"
VK_GROUP_ID = "-206831434"
CHAT_ID = "7171062856"

LAST_POST_ID = None

def get_latest_posts(group_id, count=5):
    url = "https://api.vk.com/method/wall.get"
    params = {
        "access_token": VK_ACCESS_TOKEN,
        "owner_id": group_id,
        "count": count,
        "filter": "owner",
        "extended": 1,
        "v": "5.131"
    }
    response = requests.get(url, params=params).json()
    if "response" in response:
        posts = response["response"]["items"]
        return posts
    else:
        print("ОШИБКА:", response)
        return []

# Функция для отправки фотографии из поста
async def send_photo_from_post(context: ContextTypes.DEFAULT_TYPE, post):
    if "attachments" in post:
        for attachment in post["attachments"]:
            if attachment["type"] == "photo":
                max_size = max(attachment["photo"]["sizes"], key=lambda x: x["width"])
                photo_url = max_size["url"]
                await context.bot.send_photo(chat_id=CHAT_ID, photo=photo_url)  # Используем bot из context
                break  # Отправляем только одно фото из поста

# Функция для периодической проверки новых постов
async def check_new_posts(context: ContextTypes.DEFAULT_TYPE):
    global LAST_POST_ID  # Используем глобальную переменную
    posts = get_latest_posts(VK_GROUP_ID, count=1)  # Загружаем несколько постов

    if not posts:
        print("Не удалось получить посты при периодической проверке.")
        return

    for post in reversed(posts):  # Обрабатываем посты в обратном порядке (от старых к новым)
        if LAST_POST_ID is None or post['id'] > LAST_POST_ID: # Проверяем, нужно ли отправлять пост
            await send_photo_from_post(context, post)  # Отправляем фотографию
            LAST_POST_ID = post['id']  # Обновляем ID последнего поста
            print(f"Отправлен новый пост ID: {LAST_POST_ID}")

    print("Проверка новых постов завершена.")

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Начинаю проверку постов. Я сканирую посты каждые 5 минут проявите терпение! чтобы получить расписание используйте /photo")
    await check_new_posts(context)

# Функция для инициализации фоновой задачи
async def post_init(application: Application):
    # Получаем первый пост при запуске бота.
    global LAST_POST_ID
    posts = get_latest_posts(VK_GROUP_ID, count=1)
    if posts:
        LAST_POST_ID = posts[0]['id']
        print(f"Инициализирован LAST_POST_ID: {LAST_POST_ID}")
    else:
        print("Не удалось получить посты при инициализации.")

    application.job_queue.run_repeating(check_new_posts, interval=300, first=5)


async def send_latest_posts(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    posts = get_latest_posts(VK_GROUP_ID, count=1)
    if not posts:
        await update.message.reply_text("Не удалось получить посты.")
        return

    for post in posts:
        if "attachments" in post:
            media_group = []
            for attachment in post["attachments"]:
                if attachment["type"] == "photo":
                    max_size = max(attachment["photo"]["sizes"], key=lambda x: x["width"])
                    photo_url = max_size["url"]
                    media_group.append(InputMediaPhoto(media=photo_url))

            if media_group:
                await context.bot.send_media_group(chat_id=update.message.chat_id, media=media_group)

def main() -> None:
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).post_init(post_init).build()

    # Регистрация обработчиков команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("photo", send_latest_posts))

    # Запуск бота
    application.run_polling()


if __name__ == "__main__":
    main()