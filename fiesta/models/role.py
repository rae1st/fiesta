from typing import Optional
from datetime import datetime
from ..utils import snowflake_time


class Role:
    def __init__(self, data: dict):
        self.id = int(data.get("id", 0))
        self.name = data.get("name", "")
        self.color = data.get("color", 0)
        self.hoist = data.get("hoist", False)
        self.icon = data.get("icon")
        self.unicode_emoji = data.get("unicode_emoji")
        self.position = data.get("position", 0)
        self.permissions = data.get("permissions", "0")
        self.managed = data.get("managed", False)
        self.mentionable = data.get("mentionable", False)
        self.tags = data.get("tags", {})
        self.flags = data.get("flags", 0)

    @property
    def created_at(self) -> datetime:
        return snowflake_time(self.id)

    @property
    def mention(self) -> str:
        return f"<@&{self.id}>"

    @property
    def color_hex(self) -> str:
        return f"#{self.color:06x}"

    @property
    def is_default(self) -> bool:
        return self.position == 0

    @property
    def is_bot_managed(self) -> bool:
        return "bot_id" in self.tags

    @property
    def is_booster_role(self) -> bool:
        return "premium_subscriber" in self.tags

    @property
    def is_integration_role(self) -> bool:
        return "integration_id" in self.tags

    @property
    def is_subscription_role(self) -> bool:
        return "subscription_listing_id" in self.tags

    @property
    def icon_url(self) -> Optional[str]:
        if not self.icon:
            return None
        return f"https://cdn.discordapp.com/role-icons/{self.id}/{self.icon}.png"

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"<Role id={self.id} name='{self.name}'>"
      
