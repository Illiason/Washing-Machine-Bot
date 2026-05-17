from aiogram.types import CallbackQuery

from core.database.db_manager import Database
from core.keyboards.user_keyboards import *


async def callbacks_handler(callback: CallbackQuery):
    callback_data = callback.data.split(":")

    await callback.message.delete()

    if "show" in callback_data:

        if callback_data[1] == "queue":
            db = Database(["core", "database", "database.db"], "BotDB")

            queue = await db.queue_list()
            if queue:
                await callback.message.answer(f"Current queue:\n\n{queue}")
            else:
                await callback.message.answer("Right now the queue is empty.\nUse <b><i>/queue</i></b> to take a place.")

        elif callback_data[1] == "time_selector":
            # TODO: kkkkkkkkkkkkkmausi DELETE MESSAGE
            db = Database(["core", "database", "database.db"], "BotDB")

            next_time_available = await db.next_time_available()

            await callback.message.answer(f"Next time available: <b>{next_time_available}</b>\n\n"
                                          f"Select start-time that you would like to take:\n",
                                          reply_markup=await time_start_selector_buttons(next_time_available))

    elif "select" in callback_data:

        if "time_start" in callback_data:
            time_start = int(callback_data[2])

            await callback.message.answer(f"Your start-time is <b><i>{time_start}:00</i></b>\n\nSelect a "
                                          f"finish-time:\n<i>(!) At this time you have to make washing machine "
                                          f"free.</i>",
                                          reply_markup=await time_finish_selector_buttons(f"{time_start + 1}:00"))

        elif "time_finish" in callback_data:
            start_time = callback_data[-1].split("-")[0].split("_")[0]
            finish_time = callback_data[-1].split("-")[1].split("_")[0]

            await callback.message.answer(f"<b>Start-time</b>: <b><i>{start_time}:00</i></b>\n"
                                          f"<b>Finish-time</b>: <b><i>{finish_time}:00</i></b>\n"
                                          f"\nDo you want to take this time?",
                                          reply_markup=await time_selection_submit_btn(start_time, finish_time))

    elif "cancel" in callback_data:
        if "time_selection" in callback_data:
            await callback.message.answer(f"Okay, if you want to try again, send me /queue command.")

    elif "submit" in callback_data:
        if "time_selection" in callback_data:

            db = Database(["core", "database", "database.db"], "BotDB")

            start_time = callback_data[-1].split("-")[0].split("_")[0]
            finish_time = callback_data[-1].split("-")[1].split("_")[0]

            if await db.add_to_queue(callback.from_user.id, "washing1", start_time, finish_time):
                await callback.message.answer(f"Done! Your time is {start_time}:00 - {finish_time}:00\n"
                                              f"To check your time just enter <b><i>/my_time</i></b>")
            else:
                await callback.message.answer(f"You already have your time for today.\n"
                                              f"Try again after 00:00 with /queue.")

    elif "finish" in callback_data:
        if "time" in callback_data:
            if "agree" in callback_data:
                await callback.message.answer(f"<b>Are you sure</b> that you want to "
                                              f"<b>delete</b> your place in queue?",
                                              reply_markup=await my_time_menu_delete_accept())

            elif "cancel_t" in callback_data:
                await callback.message.answer(f"Good, use <b>/my_time</b> to check your current available time.")

            elif "delete" in callback_data:
                db = Database(["core", "database", "database.db"], "BotDB")

                await db.delete_from_queue(callback.from_user.id)
                await callback.message.answer(f"Your place <b>was deleted</b>.\nUse <b>/queue</b> to take new time.")

            elif "close" in callback_data:
                await callback.message.answer("Fine, i will let you know when your time is over.")

    else:
        await callback.message.answer("Sorry, something went wrong..")

    await callback.answer()
