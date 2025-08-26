from __future__ import annotations
from typing import Callable, Any, Optional, Union
import uuid


class SelectOption:
    def __init__(
        self,
        label: str,
        value: str,
        description: Optional[str] = None,
        emoji: Optional[str] = None,
        default: bool = False,
    ):
        self.label = label
        self.value = value
        self.description = description
        self.emoji = emoji
        self.default = default

    def to_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = {
            "label": self.label,
            "value": self.value,
            "default": self.default,
        }

        if self.description:
            data["description"] = self.description

        if self.emoji:
            if self.emoji.startswith("<") and ":" in self.emoji:
                try:
                    parts = self.emoji.strip("<>").split(":")
                    animated = parts[0].startswith("a")
                    name = parts[1] if len(parts) > 1 else None
                    emoji_id = parts[2] if len(parts) > 2 else None
                    data["emoji"] = {"id": emoji_id, "name": name, "animated": animated}
                except Exception:
                    data["emoji"] = {"name": self.emoji}
            else:
                data["emoji"] = {"name": self.emoji}

        return data


class Select:
    def __init__(
        self,
        placeholder: str,
        options: list[Union[dict[str, Any], SelectOption]],
        callback: Callable[..., Any],
        min_values: int = 1,
        max_values: int = 1,
        disabled: bool = False,
        custom_id: Optional[str] = None,
    ):
        if len(options) > 25:
            raise ValueError("Select menus cannot have more than 25 options.")

        self.placeholder = placeholder
        self.options: list[SelectOption] = [
            SelectOption(**opt) if isinstance(opt, dict) else opt for opt in options
        ]
        self.callback = callback
        self.min_values = min_values
        self.max_values = max_values
        self.disabled = disabled
        self.custom_id = custom_id or f"{placeholder.lower().replace(' ', '_')}_{uuid.uuid4().hex[:6]}"

    def to_dict(self) -> dict[str, Any]:
        return {
            "type": 3,
            "custom_id": self.custom_id,
            "placeholder": self.placeholder,
            "min_values": self.min_values,
            "max_values": self.max_values,
            "disabled": self.disabled,
            "options": [opt.to_dict() for opt in self.options],
        }

    def add_option(
        self,
        label: str,
        value: str,
        description: Optional[str] = None,
        emoji: Optional[str] = None,
        default: bool = False,
    ) -> Select:
        if len(self.options) >= 25:
            raise ValueError("Select menus cannot have more than 25 options.")
        option = SelectOption(label, value, description, emoji, default)
        self.options.append(option)
        return self

    @classmethod
    def from_options(
        cls,
        placeholder: str,
        callback: Callable[..., Any],
        options: Optional[dict[str, str]] = None,
        **kwargs: str,
    ) -> Select:
        option_list: list[dict[str, Any]] = []
        source = options or kwargs
        for value, label in source.items():
            option_list.append({"label": label, "value": value})
        return cls(placeholder, option_list, callback)
