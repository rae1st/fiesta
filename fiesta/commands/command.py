from __future__ import annotations
from typing import Callable, Any
import inspect
from .parser import CommandParser


class Command:
    """Hybrid command (prefix + slash)"""

    def __init__(
        self,
        name: str,
        callback: Callable[..., Any],
        description: str | None = None,
        aliases: list[str] | None = None,
        hidden: bool = False,
    ):
        self.name = name
        self.callback = callback
        self.description = description or f"Execute {name} command"
        self.aliases = frozenset(aliases or [])
        self.hidden = hidden
        self.parser = CommandParser(callback)

    @property
    def signature(self) -> str:
        return f"{self.name}{self.parser.signature}"

    @property
    def help(self) -> str:
        return self.description

    async def invoke(self, ctx, *args, **kwargs):
        try:
            parsed_args = await self.parser.parse(ctx, args)
            if inspect.iscoroutinefunction(self.callback):
                return await self.callback(ctx, **parsed_args)
            return self.callback(ctx, **parsed_args)
        except Exception as e:
            raise e

    def to_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "name": self.name,
            "description": self.description,
            "type": 1,
            "options": self.parser.to_options(),
        }
        if self.aliases:
            payload["aliases"] = list(self.aliases)
        return payload
      
