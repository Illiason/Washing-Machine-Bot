from aiogram.types import Message

from core.keyboards.user_keyboards import *
from core.database.db_manager import Database


async def start_cmd(message: Message):
    db = Database(["core", "database", "database.db"], "BotDB")
    if message.chat.type == "private":
        if await db.create_user(message):
            await message.answer(f"Welcome, <b>{message.from_user.first_name}</b>, i will help you with queue!")
        else:
            await message.answer(f"Welcome back, <b>{message.from_user.first_name}</b>, i will help you with "
                                 f"<b><i>/queue</i></b>!")
    else:
        await message.reply(f"<b>{message.from_user.first_name}</b>, i am shy to talk in public chats..\n\
                            Text me in private!")


async def queue_cmd(message: Message):
    await message.answer(f"Select an action:", reply_markup=await queue_action_choice())


async def my_time_cmd(message: Message):
    db = Database(["core", "database", "database.db"], "BotDB")

    time_range = await db.check_time(message.from_user.id)

    if time_range:
        await message.answer(f"Start-time: <b><i>{time_range[0]}</i></b>\nExit-time: <b><i>{time_range[1]}</i></b>\n"
                             f"\n<i>(!) Make sure to make washing machine free at exit-time</i>",
                             reply_markup=await my_time_menu_btn())
    else:
        await message.answer(f"<b>{message.from_user.first_name}</b>, you don`t have a place in queue yet. "
                             f"Try to use <b>/queue</b> command to take a place!")
