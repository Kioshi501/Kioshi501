from telethon import events
from telethon.utils import get_display_name

@events.register(events.NewMessage(pattern='\.userinfo (\S+)'))
async def userinfo(event):
    args = event.pattern_match.group(1)
    try:
        user = await event.client.get_entity(args)
        if user:
            name = get_display_name(user)
            uid = user.id
            is_bot = user.is_bot
            is_self = await event.client.is_me(user)
            username = user.username if user.username else "None"
            await event.reply(f"""Информация о пользователе:
        Имя: {name}
        ID: {uid}
        Username: @{username}
        Бот: {is_bot}
        Сам пользователь: {if_self}""")
            else:
                await event.reply("Пользователь не найден.")
                except Exception as e:
                    await evet.reply(f"Ошибка: {e}")