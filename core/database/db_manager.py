import os
import asyncio
from datetime import datetime

import aiosqlite
from aiogram import Bot
from aiogram.types import Message


class Database:
    def __init__(self, path: list, name: str):
        self.name = name
        self.path = str(os.path.join(*path))

    async def user_exists(self, message: Message) -> bool:
        async with aiosqlite.connect(self.path) as db:
            print(f"\n[ INFO ] CONNECTED TO DATABASE: {self.path}")

            telegram_id = message.from_user.id

            cursor = await db.execute(f"SELECT * FROM users WHERE telegram_id={telegram_id}")
            result = await cursor.fetchone()

            print(f"\n[ INFO ] SEARCHED FOR USER: {telegram_id} ({bool(result)})\n")

            return True if result else False

    async def create_user(self, message: Message) -> bool:
        if not await self.user_exists(message):
            async with aiosqlite.connect(self.path) as db:
                print(f"\n[ INFO ] CONNECTED TO DATABASE: {self.path}")

                telegram_id = message.from_user.id
                name = message.from_user.first_name

                await db.execute(f"INSERT INTO users VALUES ({telegram_id}, \"{name}\")")
                await db.commit()

                print(f"[ INFO ] CREATED USER:\n\tID: {telegram_id}\n\tNAME: {name}\n")

                return True
        else:
            return False

    async def user_in_queue(self, telegram_id: int) -> bool:
        async with aiosqlite.connect(self.path) as db:
            print(f"\n[ INFO ] CONNECTED TO DATABASE: {self.path}")

            cursor = await db.execute(f"SELECT * FROM washing1 WHERE telegram_id = {telegram_id}")
            result = await cursor.fetchone()
            print(f"telegram_id={telegram_id}, result={result}")

            return True if result else False

    async def add_to_queue(self, telegram_id: int, machine: str, start_time: str, finish_time: str) -> bool:
        if not await self.user_in_queue(telegram_id):
            async with aiosqlite.connect(self.path) as db:
                print(f"\n[ INFO ] CONNECTED TO DATABASE: {self.path}")

                start_time += ":00"
                finish_time += ":00"

                if start_time[1] == ":":
                    start_time = f"0{start_time}"

                if finish_time[1] == ":":
                    finish_time = f"0{finish_time}"

                await db.execute(f"INSERT INTO washing1 VALUES ({telegram_id}, \"{start_time}\", \"{finish_time}\")")
                await db.commit()

                print(f"[ INFO ] ADDED USER TO QUE:\n\tID: {telegram_id}\n\tTIME RANGE: {start_time} - {finish_time}\n")

                return True
        else:
            return False

    async def next_time_available(self) -> str:
        async with aiosqlite.connect(self.path) as db:
            print(f"\n[ INFO ] CONNECTED TO DATABASE: {self.path}")

            cursor = await db.execute("SELECT exit_time FROM washing1")
            first_result = await cursor.fetchall()

            if first_result:
                result = []

                for i in range(len(first_result)):
                    result.append(first_result[i][0])

                print(f"[ INFO ] SEARCHED FOR NEXT FREE TIME FOUND: {max(result)}")

                return max(result)
            else:
                now = datetime.now()

                print(f"[ INFO ] SEARCHED FOR NEXT FREE TIME FOUND: {now.strftime('%H:00')}")

                return now.strftime("%H:00")

    async def clear_db(self, bot: Bot):
        async with aiosqlite.connect(self.path) as db:
            print(f"\n[ INFO ] CONNECTED TO DATABASE: {self.path}")

            while True:
                now = datetime.now()
                print(f"\n[ INFO ] CHECKED TIME ({now.strftime('%H:%M')})")

                cursor = await db.execute("SELECT telegram_id, exit_time FROM washing1")
                result = await cursor.fetchall()

                for row in result:
                    if row[-1] == now.strftime("%H:%M"):
                        await self.delete_from_queue(row[0])

                        print(f"\n[ INFO ] DELETED FROM washing1:\n\tTELEGRAM ID: {row[0]}\n\tEXIT TIME: {row[1]}\n")

                        await bot.send_message(row[0], "<b>Your time is over.</b>\n\n"
                                                       "Make sure to make washing machine free! ^_^")

                if now.strftime("%H:%M") == "00:00":
                    await db.execute("DELETE FROM washing1")
                    await db.commit()

                    print(f"\n[ INFO ] (!!!) DELETED ALL ROWS FROM WASHING1 ({now.strftime('%H:%M')})")

                await asyncio.sleep(60)

    async def check_time(self, telegram_id: int) -> list:
        async with aiosqlite.connect(self.path) as db:
            print(f"\n[ INFO ] CONNECTED TO DATABASE: {self.path}")

            cursor = await db.execute(f"SELECT entry_time, exit_time FROM washing1 WHERE telegram_id={telegram_id}")
            result = await cursor.fetchone()

            return result

    async def delete_from_queue(self, telegram_id: int):
        async with aiosqlite.connect(self.path) as db:
            print(f"\n[ INFO ] CONNECTED TO DATABASE: {self.path}")

            await db.execute(f"DELETE FROM washing1 WHERE telegram_id={telegram_id}")
            await db.commit()

    async def queue_list(self) -> str:
        async with aiosqlite.connect(self.path) as db:
            print(f"\n[ INFO ] CONNECTED TO DATABASE: {self.path}")

            cursor = await db.execute("SELECT * FROM washing1")
            result = await cursor.fetchall()

            result_formatted = ""

            for i in range(len(result)):
                username = await self.user_info(result[i][0])
                result_formatted += f"{i+1}. <b>{username}</b>: {result[i][1]} - {result[i][2]}\n"

            return result_formatted

    async def user_info(self, telegram_id: int) -> str:
        async with aiosqlite.connect(self.path) as db:
            print(f"\n[ INFO ] CONNECTED TO DATABASE: {self.path}")

            cursor = await db.execute(f"SELECT name FROM users WHERE telegram_id={telegram_id}")
            result = await cursor.fetchone()

            return result[0]


if __name__ == "__main__":
    database = Database(["..", "database", "database.db"], "TestDB")
    print(asyncio.run(database.next_time_available()))
