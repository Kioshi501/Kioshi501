# mybigmodule.py

# Импорт необходимых библиотек
from userbot import loader, utils
from telethon import events
from telethon.tl.functions.contacts import BlockRequest, UnblockRequest
import asyncio
import random
import aiohttp
import datetime
import os
import platform

@loader.tds
class MyBigModule(loader.Module):
    """Большой модуль для Hikka Userbot с множеством функций."""

    strings = {
        "name": "MyBigModule",
        "ping": "<b>🏓 Понг!</b> <code>{} ms</code>",
        "echo_usage": "<b>Использование:</b> <code>.echo [текст]</code>",
        "ban_success": "<b>🔨 Пользователь {}</b> <b>заблокирован.</b>",
        "unban_success": "<b>✅ Пользователь {}</b> <b>разблокирован.</b>",
        "kick_success": "<b>🔨 Пользователь {}</b> <b>выгнан из чата.</b>",
        "meme_loading": "<b>🔄 Загружаю мем...</b>",
        "meme_error": "<b>❌ Не удалось загрузить мем.</b>",
        "quote_loading": "<b>🔄 Загружаю цитату...</b>",
        "quote_error": "<b>❌ Не удалось загрузить цитату.</b>",
        "translate_usage": "<b>❌ Использование:</b> <code>.translate [язык] [текст]</code>",
        "translate_error": "<b>❌ Не удалось выполнить перевод.</b>",
        "currency_usage": "<b>❌ Использование:</b> <code>.currency [сумма] [из] [в]</code>",
        "currency_error": "<b>❌ Не удалось конвертировать валюту.</b>",
        "info_user": (
            "<b>👤 Информация о пользователе:</b>\n\n"
            "• <b>Имя:</b> {first} {last}\n"
            "• <b>Username:</b> @{username}\n"
            "• <b>ID:</b> <code>{id}</code>\n"
            "• <b>Bio:</b> {bio}"
        ),
        "info_chat": (
            "<b>📋 Информация о чате:</b>\n\n"
            "• <b>Название:</b> {title}\n"
            "• <b>Тип:</b> {type}\n"
            "• <b>ID:</b> <code>{id}</code>\n"
            "• <b>Участников:</b> {members}"
        ),
        "sysinfo": (
            "<b>🖥️ Системная информация:</b>\n\n"
            "• <b>Система:</b> {system}\n"
            "• <b>Имя узла:</b> {node}\n"
            "• <b>Версия:</b> {version}\n"
            "• <b>Машина:</b> {machine}\n"
            "• <b>Процессор:</b> {processor}\n"
        ),
        "download_success": "<b>📦 Файл успешно скачан.</b>",
        "download_error": "<b>❌ Не удалось скачать файл.</b>",
        "help_text": (
            "<b>📚 Доступные команды модуля MyBigModule:</b>\n\n"
            "• <b>.ping</b> - Проверяет задержку бота.\n"
            "• <b>.echo [текст]</b> - Повторяет ваше сообщение.\n"
            "• <b>.ban</b> - Блокирует пользователя (нужен реплай на сообщение).\n"
            "• <b>.unban [username или ID]</b> - Разблокирует пользователя.\n"
            "• <b>.kick</b> - Выгоняет пользователя из чата (нужен реплай на сообщение).\n"
            "• <b>.meme</b> - Отправляет случайный мем.\n"
            "• <b>.quote</b> - Отправляет случайную цитату.\n"
            "• <b>.translate [язык] [текст]</b> - Переводит текст на указанный язык.\n"
            "• <b>.currency [сумма] [из] [в]</b> - Конвертирует валюту.\n"
            "• <b>.info</b> - Получает информацию о пользователе или чате.\n"
            "• <b>.sysinfo</b> - Получает системную информацию о сервере.\n"
            "• <b>.download</b> - Скачивает файл из сообщения.\n"
            "• <b>.helpme</b> - Отображает это сообщение.\n"
        ),
    }

    @loader.command()
    async def ping(self, m):
        """Проверяет задержку бота."""
        start = datetime.datetime.now()
        msg = await m.respond("<b>🏓 Пинг...</b>")
        end = datetime.datetime.now()
        delta = (end - start).microseconds / 1000
        await msg.edit(self.strings["ping"].format(delta))

    @loader.command()
    async def echo(self, m):
        """Повторяет ваше сообщение."""
        args = utils.get_args_raw(m)
        if not args:
            await m.edit(self.strings["echo_usage"])
            return
        await m.delete()
        await m.client.send_message(m.chat_id, args)

    @loader.command()
    async def ban(self, m):
        """Блокирует пользователя."""
        reply = await m.get_reply_message()
        if not reply:
            await m.edit("<b>❌ Нужно ответить на сообщение пользователя для блокировки.</b>")
            return
        user = reply.sender
        if not user:
            await m.edit("<b>❌ Не удалось определить пользователя.</b>")
            return
        try:
            await m.client(BlockRequest(user.id))
            await m.edit(self.strings["ban_success"].format(user.first_name))
        except Exception as e:
            await m.edit(f"<b>❌ Ошибка при блокировке:</b> {e}")

    @loader.command()
    async def unban(self, m):
        """Разблокирует пользователя."""
        args = utils.get_args_raw(m)
        if not args:
            await m.edit("<b>❌ Нужно указать ID или @username пользователя для разблокировки.</b>")
            return
        try:
            user = await m.client.get_entity(args)
            await m.client(UnblockRequest(user.id))
            await m.edit(self.strings["unban_success"].format(user.first_name))
        except Exception as e:
            await m.edit(f"<b>❌ Произошла ошибка:</b> {e}")

    @loader.command()
    async def kick(self, m):
        """Выгоняет пользователя из чата."""
        reply = await m.get_reply_message()
        if not reply:
            await m.edit("<b>❌ Нужно ответить на сообщение пользователя для кика.</b>")
            return
        user = reply.sender
        if not user:
            await m.edit("<b>❌ Не удалось определить пользователя.</b>")
            return
        try:
            await m.client.kick_participant(m.chat_id, user.id)
            await m.edit(self.strings["kick_success"].format(user.first_name))
        except Exception as e:
            await m.edit(f"<b>❌ Не удалось выгнать пользователя:</b> {e}")

    @loader.command()
    async def meme(self, m):
        """Отправляет случайный мем."""
        await m.edit(self.strings["meme_loading"])
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get("https://meme-api.com/gimme") as resp:
                    if resp.status != 200:
                        await m.edit(self.strings["meme_error"])
                        return
                    data = await resp.json()
                    meme_url = data.get("url")
                    meme_caption = data.get("title")
                    if not meme_url:
                        await m.edit(self.strings["meme_error"])
                        return
                    await m.client.send_file(m.chat_id, meme_url, caption=meme_caption)
                    await m.delete()
        except Exception as e:
            await m.edit(f"<b>❌ Ошибка при получении мема:</b> {e}")

    @loader.command()
    async def quote(self, m):
        """Отправляет случайную цитату."""
        await m.edit(self.strings["quote_loading"])
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get("https://api.quotable.io/random") as resp:
                    if resp.status != 200:
                        await m.edit(self.strings["quote_error"])
                        return
                    data = await resp.json()
                    content = data.get("content")
                    author = data.get("author")
                    if not content:
                        await m.edit(self.strings["quote_error"])
                        return
                    await m.edit(f"<b>📝 Цитата:</b>\n\n<code>{content}</code>\n\n<b>— {author}</b>")
        except Exception as e:
            await m.edit(f"<b>❌ Ошибка при получении цитаты:</b> {e}")

    @loader.command()
    async def translate(self, m):
        """Переводит текст. Использование: .translate [язык] [текст]"""
        args = utils.get_args_raw(m)
        if not args:
            await m.edit(self.strings["translate_usage"])
            return
        parts = args.split(' ', 1)
        if len(parts) < 2:
            await m.edit(self.strings["translate_usage"])
            return
        lang, text = parts
        await m.edit("<b>🔄 Перевожу...</b>")
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"https://api.mymemory.translated.net/get?q={text}&langpair=auto|{lang}"
                ) as resp:
                    if resp.status != 200:
                        await m.edit(self.strings["translate_error"])
                        return
                    data = await resp.json()
                    translated_text = data.get("responseData", {}).get("translatedText")
                    if not translated_text:
                        await m.edit(self.strings["translate_error"])
                        return
                    await m.edit(f"<b>📜 Перевод ({lang}):</b>\n<code>{translated_text}</code>")
        except Exception as e:
            await m.edit(f"<b>❌ Ошибка при переводе:</b> {e}")

    @loader.command()
    async def currency(self, m):
        """Конвертирует валюту. Использование: .currency [сумма] [из] [в]"""
        args = utils.get_args_raw(m)
        if not args:
            await m.edit(self.strings["currency_usage"])
            return
        parts = args.split()
        if len(parts) != 3:
            await m.edit(self.strings["currency_usage"])
            return
        amount, from_currency, to_currency = parts
        try:
            amount = float(amount)
        except ValueError:
            await m.edit("<b>❌ Сумма должна быть числом.</b>")
            return
        await m.edit("<b>🔄 Конвертирую валюту...</b>")
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"https://api.exchangerate-api.com/v4/latest/{from_currency.upper()}") as resp:
                    if resp.status != 200:
                        await m.edit(self.strings["currency_error"])
                        return
                    data = await resp.json()
                    rates = data.get("rates")
                    if not rates or to_currency.upper() not in rates:
                        await m.edit("<b>❌ Неверный код валюты.</b>")
                        return
                    rate = rates[to_currency.upper()]
                    converted = amount * rate
                    await m.edit(f"<b>💱 {amount} {from_currency.upper()} = {converted} {to_currency.upper()}</b>")
        except Exception as e:
            await m.edit(f"<b>❌ Ошибка при конвертации валюты:</b> {e}")

    @loader.command()
    async def info(self, m):
        """Получает информацию о пользователе или чате."""
        reply = await m.get_reply_message()
        if reply and reply.sender:
            user = reply.sender
            try:
                username = user.username or "Не установлено"
                first = user.first_name or ""
                last = user.last_name or ""
                bio = user.about or "Нет информации"
                await m.edit(
                    self.strings["info_user"].format(
                        first=first,
                        last=last,
                        username=username,
                        id=user.id,
                        bio=bio
                    )
                )
            except Exception as e:
                await m.edit(f"<b>❌ Ошибка при получении информации о пользователе:</b> {e}")
        else:
            try:
                chat = await m.get_chat()
                participants = await m.client.get_participants(chat)
                members = len(participants)
                await m.edit(
                    self.strings["info_chat"].format(
                        title=chat.title,
                        type=type(chat).__name__,
                        id=chat.id,
                        members=members
                    )
                )
            except Exception as e:
                await m.edit(f"<b>❌ Ошибка при получении информации о чате:</b> {e}")

    @loader.command()
    async def sysinfo(self, m):
        """Получает системную информацию о сервере."""
        uname = platform.uname()
        info = self.strings["sysinfo"].format(
            system=uname.system,
            node=uname.node,
            version=uname.version,
            machine=uname.machine,
            processor=uname.processor
        )
        await m.edit(info)

    @loader.command()
    async def download(self, m):
        """Скачивает файлы из сообщений. Использование: .download [реплай на сообщение с файлом]"""
        reply = await m.get_reply_message()
        if not reply or not reply.media:
            await m.edit("<b>❌ Нужно ответить на сообщение с файлом для скачивания.</b>")
            return
        await m.edit("<b>🔄 Скачиваю файл...</b>")
        try:
            file_path = await reply.download_media()
            await m.client.send_file(m.chat_id, file_path, caption=self.strings["download_success"])
            os.remove(file_path)
            await m.delete()
        except Exception as e:
            await m.edit(f"<b>❌ Не удалось скачать файл:</b> {e}")

    @loader.command()
    async def helpme(self, m):
        """Отображает список доступных команд модуля."""
        await m.edit(self.strings["help_text"])

    async def client_ready(self, client, db):
        """Вызывается, когда клиент готов."""
        self.client = client
        self.db = db
        # Инициализация при необходимости