from hikka import Module, Command, MessageEvent, Client
import datetime

class UtilityModule(Module):
    name = "utility"

    @Command(names=["/hello", "/hi"], description="Приветствует пользователя.")
    async def hello_command(self, event: MessageEvent):
        await event.reply(f"Привет, {event.sender.first_name}!")

    @Command(names=["/time"], description="Показывает текущее время.")
    async def time_command(self, event: MessageEvent):
        now = datetime.datetime.now()
        formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")
        await event.reply(f"Текущее время: {formatted_time}")


def setup(client: Client):
    client.add_module(UtilityModule)