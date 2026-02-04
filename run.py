import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.session.aiohttp import AiohttpSession

from core.handlers.register import register_handlers
from core.utils.commands import set_commands

from core.database.db_manager import Database

TOKEN = getenv("BOT_TOKEN")

session = AiohttpSession(proxy="http://proxy.server:3128")

bot = Bot(TOKEN, parse_mode=ParseMode.HTML, session=session)
dp = Dispatcher()

db = Database(["core", "database", "database.db"], "RunDB")


async def main():
    reg_handlers = asyncio.create_task(register_handlers(dp))
    set_cmd_menu = asyncio.create_task(set_commands(bot))
    dp_start_polling = asyncio.create_task(dp.start_polling(bot))
    clean_db = asyncio.create_task(db.clear_db(bot))

    await asyncio.gather(reg_handlers, set_cmd_menu, dp_start_polling, clean_db)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
