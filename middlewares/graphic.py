from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message
from misc.graphic import Graphic


class GraphicMiddleware(BaseMiddleware):
    def __init__(self, graphic: Graphic) -> None:
        self.graphic = graphic

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        data["graphic"] = self.graphic

        result = await handler(event, data)
        return result
