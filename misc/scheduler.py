import asyncio
from datetime import datetime

from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from database.repo.requests import RequestsRepo
from misc.graphic import Graphic
from misc.shutdown_info import get_information_about_graphic


async def monitor_graphic(graphic: Graphic, session_pool, bot: Bot):
    is_updated = await graphic.update_graphic()

    if is_updated:
        async with (session_pool() as session):
            repo = RequestsRepo(session)
            users = await repo.users.get_user_with_getting_update()

            date_now = datetime.now()
            update_time = date_now.strftime("%H:%M")
            text_to_send = f"<b>{update_time}</b>" + \
                           " Графік оновлено.\n\n"

            for user in users:
                if not user.get_update:
                    continue
                unique_text_to_send = text_to_send + get_information_about_graphic(
                    user.group,
                    graphic
                ) + "\n\n" + graphic.pprint_row(user.group)
                await bot.send_message(user.telegram_id, unique_text_to_send, parse_mode="HTML")
                await asyncio.sleep(0.05)


async def start_scheduler(graphic: Graphic, session_pool, bot):
    scheduler = AsyncIOScheduler()
    scheduler.add_job(monitor_graphic, "interval", args=[graphic, session_pool, bot], minutes=10)
    scheduler.start()
