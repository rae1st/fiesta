from __future__ import annotations
from typing import Optional
from datetime import datetime
from ..utils import snowflake_time


class User:
    def __init__(self, data: dict):
        self.id: int = int(data.get("id", 0))
        self.username: str = data.get("username", "")
        self.discriminator: str = data.get("discriminator", "0000")
        self.global_name: Optional[str] = data.get("global_name")
        self.avatar: Optional[str] = data.get("avatar")
        self.avatar_decoration: Optional[str] = data.get("avatar_decoration_data")
        self.bot: bool = data.get("bot", False)
        self.system: bool = data.get("system", False)
        self.verified: bool = data.get("verified", False)
        self.email: Optional[str] = data.get("email")
        self.flags: int = data.get("flags", 0)
        self.premium_type: int = data.get("premium_type", 0)
        self.public_flags: int = data.get("public_flags", 0)

    @property
    def display_name(self) -> str:
        return self.global_name or self.username

    @property
    def mention(self) -> str:
        return f"<@{self.id}>"

    @property
    def tag(self) -> str:
        if self.discriminator == "0":
            return self.username
        return f"{self.username}#{self.discriminator}"

    @property
    def created_at(self) -> Optional[datetime]:
        try:
            return snowflake_time(self.id)
        except Exception:
            return None

    @property
    def avatar_url(self) -> Optional[str]:
        if not self.avatar:
            return None
        ext = "gif" if self.avatar.startswith("a_") else "png"
        return f"https://cdn.discordapp.com/avatars/{self.id}/{self.avatar}.{ext}?size=1024"

    @property
    def avatar_decoration_url(self) -> Optional[str]:
        if not self.avatar_decoration:
            return None
        asset = self.avatar_decoration.get("asset")
        if asset:
            return f"https://cdn.discordapp.com/avatar-decorations/{self.id}/{asset}.png"
        return None

    @property
    def default_avatar_url(self) -> str:
        if self.discriminator == "0":
            index = (self.id >> 22) % 6
        else:
            index = int(self.discriminator) % 5
        return f"https://cdn.discordapp.com/embed/avatars/{index}.png"

    @property
    def display_avatar_url(self) -> str:
        return self.avatar_url or self.default_avatar_url

    def __str__(self) -> str:
        return self.tag

    def __repr__(self) -> str:
        return f"<User id={self.id} name='{self.username}' discriminator='{self.discriminator}'>"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, User):
            return self.id == other.id
        return False

    def __hash__(self) -> int:
        return hash(self.id)
      
