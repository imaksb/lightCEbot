from aiogram import Bot, Dispatcher

from data.config import load_config
from aiogram.client.default import DefaultBotProperties
from database.setup import create_engine, create_session_pool
from misc.graphic import Graphic
from middlewares.database import DatabaseMiddleware
from middlewares.graphic import GraphicMiddleware
from routers import routers_list
from aiogram.enums import ParseMode
import logging 
import betterlogging as bl

from misc.scheduler import start_scheduler


def register_global_middlewares(dp: Dispatcher, session_pool, graphic):
    middleware_types = [
        DatabaseMiddleware(session_pool),
        GraphicMiddleware(graphic),
    ]

    for middleware_type in middleware_types:
        dp.message.outer_middleware(middleware_type)
        dp.callback_query.outer_middleware(middleware_type)


def setup_logging():
    log_level = logging.INFO
    bl.basic_colorized_config(level=log_level)

    logging.basicConfig(
        level=logging.INFO,
        format="%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s",
    )
    logger = logging.getLogger(__name__)
    logger.info("Starting bot")


async def main():
    setup_logging()

    config = load_config()

    dp = Dispatcher()
    dp.include_routers(*routers_list)

    engine = await create_engine() 
    session_pool = create_session_pool(engine)

    graphic = Graphic()
    bot = Bot(token=config.token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    await start_scheduler(graphic, session_pool, bot)

    await graphic.update_graphic()

    register_global_middlewares(dp, session_pool, graphic)

    await dp.start_polling(bot)


if __name__ == "__main__":
    import asyncio 
    asyncio.run(main())
