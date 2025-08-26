from __future__ import annotations
import inspect
from typing import Any, Callable
from ..errors import CommandError


class CommandParser:
    """Parse command arguments for hybrid commands"""

    def __init__(self, callback: Callable[..., Any]):
        self.callback = callback
        sig = inspect.signature(callback)
        # skip first param (ctx)
        self.parameters: list[inspect.Parameter] = list(sig.parameters.values())[1:]

    async def parse(self, ctx, args: tuple[str, ...]) -> dict[str, Any]:
        parsed: dict[str, Any] = {}
        args_list = list(args)

        for i, param in enumerate(self.parameters):
            if i < len(args_list):
                value = args_list[i]
                parsed[param.name] = await self._convert_argument(value, param)
            elif param.default != param.empty:
                parsed[param.name] = param.default
            else:
                raise CommandError(f"Missing required argument: {param.name}")

        return parsed

    async def _convert_argument(self, value: str, param: inspect.Parameter) -> Any:
        annotation = param.annotation
        if annotation in (param.empty, str):
            return value

        try:
            if annotation is int:
                return int(value)
            if annotation is float:
                return float(value)
            if annotation is bool:
                return value.lower() in {"true", "yes", "1", "on", "y"}
            return value
        except ValueError:
            raise CommandError(f"Invalid {annotation.__name__}: {value}")

    @property
    def signature(self) -> str:
        parts: list[str] = []
        for param in self.parameters:
            if param.default != param.empty:
                parts.append(f"[{param.name}]")
            else:
                parts.append(f"<{param.name}>")
        return f" {' '.join(parts)}" if parts else ""

    def to_options(self) -> list[dict[str, Any]]:
        options: list[dict[str, Any]] = []
        for param in self.parameters:
            options.append(
                {
                    "name": param.name,
                    "description": f"{param.name} parameter",
                    "type": self._get_option_type(param.annotation),
                    "required": param.default == param.empty,
                }
            )
        return options

    def _get_option_type(self, annotation: Any) -> int:
        if annotation in (str, inspect.Parameter.empty):
            return 3  # STRING
        if annotation is int:
            return 4  # INTEGER
        if annotation is bool:
            return 5  # BOOLEAN
        if annotation is float:
            return 10  # NUMBER
        return 3
      
