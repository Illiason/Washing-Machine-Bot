import asyncio
import logging
import sys
from os import getenv

# Import core aiogram components for bot functionality and session management
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.session.aiohttp import AiohttpSession

# Import custom project modules for handlers, commands, and database logic
from core.handlers.register import register_handlers
from core.utils.commands import set_commands
from core.database.db_manager import Database

# Retrieve the secret bot token from environment variables
TOKEN = getenv("BOT_TOKEN")

# Initialize a custom AiohttpSession to route requests through a specific proxy server
session = AiohttpSession(proxy="http://proxy.server:3128")

# Initialize the Bot object with the token, default HTML formatting, and the proxy session
bot = Bot(TOKEN, parse_mode=ParseMode.HTML, session=session)

# Initialize the Dispatcher, which acts as the main router for incoming updates
dp = Dispatcher()

# Initialize the database manager with the relative path to the SQLite file
db = Database(["core", "database", "database.db"], "RunDB")


async def main():
    """
    Asynchronous entry point that initializes bot features and starts polling.
    Tasks are wrapped in create_task to allow them to initialize concurrently.
    """
    # Schedule the registration of message and callback handlers
    reg_handlers = asyncio.create_task(register_handlers(dp))
    
    # Schedule the synchronization of bot commands with the Telegram server
    set_cmd_menu = asyncio.create_task(set_commands(bot))
    
    # Schedule the long-polling process to start receiving updates from Telegram
    dp_start_polling = asyncio.create_task(dp.start_polling(bot))
    
    # Schedule a database cleanup routine to run on startup
    clean_db = asyncio.create_task(db.clear_db(bot))

    # Wait for all scheduled tasks to be processed/running
    await asyncio.gather(reg_handlers, set_cmd_menu, dp_start_polling, clean_db)


if __name__ == "__main__":
    # Configure system logging to output INFO level logs to the standard output
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    
    # Execute the main coroutine using the asyncio event loop
    asyncio.run(main())
