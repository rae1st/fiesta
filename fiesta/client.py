import asyncio
import inspect
from typing import Optional, Dict, Any, Callable, Union, Awaitable

from .gateway import Gateway
from .http import HTTPClient
from .intents import Intents
from .commands import Command, Context
from .interactions import Button, Select, Modal
from .models import User
from .errors import LoginFailure


EventHandler = Union[Callable[..., Any], Callable[..., Awaitable[Any]]]


class Client:
    def __init__(
        self,
        command_prefix: str = "!",
        intents: Union[str, Intents] = "default",
        case_insensitive: bool = True,
    ):
        self.command_prefix = command_prefix
        self.case_insensitive = case_insensitive
        self.user: Optional[User] = None
        self.guilds: Dict[int, Any] = {}
        self.channels: Dict[int, Any] = {}
        self.users: Dict[int, User] = {}

        if isinstance(intents, str):
            self.intents = Intents.default() if intents == "default" else Intents.all()
        else:
            self.intents = intents

        self._http: Optional[HTTPClient] = None
        self._gateway: Optional[Gateway] = None
        self._events: Dict[str, list[EventHandler]] = {}
        self._commands: Dict[str, Command] = {}
        self._buttons: Dict[str, Button] = {}
        self._selects: Dict[str, Select] = {}
        self._modals: Dict[str, Modal] = {}

    def event(self, func: EventHandler) -> EventHandler:
        name = func.__name__
        self._events.setdefault(name, []).append(func)
        return func

    def command(
        self, name: Optional[str] = None, description: Optional[str] = None
    ) -> Callable[[Callable[..., Awaitable[Any]]], Command]:
        def decorator(func: Callable[..., Awaitable[Any]]) -> Command:
            cmd_name = name or func.__name__
            if self.case_insensitive:
                cmd_name = cmd_name.lower()
            cmd = Command(
                name=cmd_name,
                callback=func,
                description=description or f"Execute {cmd_name} command",
            )
            self._commands[cmd_name] = cmd
            return cmd

        return decorator

    def button(
        self, custom_id: str, style: str = "primary", emoji: Optional[str] = None
    ) -> Callable[[Callable[..., Awaitable[Any]]], Button]:
        def decorator(func: Callable[..., Awaitable[Any]]) -> Button:
            btn = Button(custom_id=custom_id, callback=func, style=style, emoji=emoji)
            self._buttons[custom_id] = btn
            return btn

        return decorator

    def select(
        self, custom_id: str, placeholder: str, options: list
    ) -> Callable[[Callable[..., Awaitable[Any]]], Select]:
        def decorator(func: Callable[..., Awaitable[Any]]) -> Select:
            sel = Select(
                custom_id=custom_id,
                placeholder=placeholder,
                options=options,
                callback=func,
            )
            self._selects[custom_id] = sel
            return sel

        return decorator

    def modal(
        self, custom_id: str, title: str, fields: list
    ) -> Callable[[Callable[..., Awaitable[Any]]], Modal]:
        def decorator(func: Callable[..., Awaitable[Any]]) -> Modal:
            mod = Modal(custom_id=custom_id, title=title, fields=fields, callback=func)
            self._modals[custom_id] = mod
            return mod

        return decorator

    async def _dispatch(self, event: str, *args, **kwargs) -> None:
        handlers = self._events.get(event)
        if not handlers:
            return
        for handler in handlers:
            try:
                if inspect.iscoroutinefunction(handler):
                    await handler(*args, **kwargs)
                else:
                    handler(*args, **kwargs)
            except Exception as e:
                if event != "error":
                    await self._dispatch("error", e)

    async def _handle_message(self, data: dict) -> None:
        content = data.get("content", "")
        if not content.startswith(self.command_prefix):
            return
        cmd_name = content[len(self.command_prefix) :].split()[0]
        if self.case_insensitive:
            cmd_name = cmd_name.lower()
        command = self._commands.get(cmd_name)
        if not command:
            return
        ctx = Context(self, data)
        try:
            await command.callback(ctx)
        except Exception as e:
            await self._dispatch("command_error", ctx, e)

    async def _handle_interaction(self, data: dict) -> None:
        interaction_type = data.get("type")
        custom_id = data.get("data", {}).get("custom_id", "")
        if interaction_type == 3:
            if custom_id in self._buttons:
                await self._buttons[custom_id].callback(data)
            elif custom_id in self._selects:
                await self._selects[custom_id].callback(data)
        elif interaction_type == 5:
            if custom_id in self._modals:
                await self._modals[custom_id].callback(data)

    async def start(self, token: str) -> None:
        self._http = HTTPClient(token)
        self._gateway = Gateway(self, token, self.intents)
        try:
            await self._http.start()
            await self._gateway.connect()
        except Exception as e:
            raise LoginFailure(f"Failed to login: {e}") from e

    def run(self, token: str) -> None:
        try:
            asyncio.run(self.start(token))
        except KeyboardInterrupt:
            pass
        finally:
            if self._gateway and not self._gateway.closed:
                asyncio.run(self._gateway.close())
            if self._http and not self._http.closed:
                asyncio.run(self._http.close())

    async def close(self) -> None:
        if self._gateway:
            await self._gateway.close()
        if self._http:
            await self._http.close()
