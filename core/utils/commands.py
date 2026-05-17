from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command="start",
            description="Start of work"
        ),
        BotCommand(
            command="queue",
            description="Actions with queue"
        ),
        BotCommand(
            command="my_time",
            description="Check my time"
        ),
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())
