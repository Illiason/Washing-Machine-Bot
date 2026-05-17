from aiogram.filters import CommandStart, Command
from aiogram import Dispatcher

from core.handlers.basic import *
from core.handlers.callback import *


async def register_handlers(dp: Dispatcher):
    dp.message.register(start_cmd, CommandStart())
    dp.message.register(queue_cmd, Command("queue"))
    dp.message.register(my_time_cmd, Command("my_time"))

    dp.callback_query.register(callbacks_handler)
