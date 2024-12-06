from hikka import Module, Command, MessageEvent, Client


class RandomModule(Module):
    name = "random"

    @Command(names=["/random"], description="Получить случайное число от 1 до 100")
    async def random_command(self, event: MessageEvent):
        import random
        random_number = random.randint(1, 100)
        await event.reply(f"Случайное число: {random_number}")


def setup(client: Client):
    client.add_module(RandomModule)