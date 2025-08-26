from __future__ import annotations
from typing import Callable, Any, Optional, Literal
import uuid


class Button:
    STYLES: dict[str, int] = {
        "primary": 1,
        "secondary": 2,
        "success": 3,
        "danger": 4,
        "link": 5,
    }

    def __init__(
        self,
        label: str,
        callback: Optional[Callable[..., Any]],
        style: Literal["primary", "secondary", "success", "danger", "link"] = "primary",
        emoji: Optional[str] = None,
        url: Optional[str] = None,
        disabled: bool = False,
        custom_id: Optional[str] = None,
    ):
        self.label = label
        self.callback = callback
        self.style = style
        self.emoji = emoji
        self.url = url
        self.disabled = disabled
        self.custom_id = custom_id or f"{label.lower().replace(' ', '_')}_{uuid.uuid4().hex[:6]}"

    def to_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = {
            "type": 2,
            "style": self.STYLES.get(self.style, 1),
            "label": self.label,
            "disabled": self.disabled,
        }

        if self.style == "link":
            if not self.url:
                raise ValueError("Link buttons must have a URL.")
            data["url"] = self.url
        else:
            data["custom_id"] = self.custom_id

        if self.emoji:
            if self.emoji.startswith("<") and ":" in self.emoji:  # custom emoji like <a:name:id>
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

    @classmethod
    def primary(cls, label: str, callback: Callable[..., Any], **kwargs) -> Button:
        return cls(label, callback, style="primary", **kwargs)

    @classmethod
    def secondary(cls, label: str, callback: Callable[..., Any], **kwargs) -> Button:
        return cls(label, callback, style="secondary", **kwargs)

    @classmethod
    def success(cls, label: str, callback: Callable[..., Any], **kwargs) -> Button:
        return cls(label, callback, style="success", **kwargs)

    @classmethod
    def danger(cls, label: str, callback: Callable[..., Any], **kwargs) -> Button:
        return cls(label, callback, style="danger", **kwargs)

    @classmethod
    def link(cls, label: str, url: str, **kwargs) -> Button:
        return cls(label, None, style="link", url=url, **kwargs)
      
