from __future__ import annotations
from typing import Optional, List
from datetime import datetime
from ..utils import snowflake_time


class Guild:
    def __init__(self, data: dict):
        self.id: int = int(data.get("id", 0))
        self.name: str = data.get("name", "")
        self.icon: Optional[str] = data.get("icon")
        self.icon_hash: Optional[str] = data.get("icon_hash")
        self.splash: Optional[str] = data.get("splash")
        self.discovery_splash: Optional[str] = data.get("discovery_splash")
        self.owner_id: Optional[int] = (
            int(data["owner_id"]) if data.get("owner_id") else None
        )
        self.permissions: Optional[str] = data.get("permissions")
        self.region: Optional[str] = data.get("region")  # deprecated
        self.rtc_region: Optional[str] = data.get("rtc_region")
        self.afk_channel_id: Optional[int] = (
            int(data["afk_channel_id"]) if data.get("afk_channel_id") else None
        )
        self.afk_timeout: Optional[int] = data.get("afk_timeout")
        self.widget_enabled: bool = data.get("widget_enabled", False)
        self.widget_channel_id: Optional[int] = (
            int(data["widget_channel_id"]) if data.get("widget_channel_id") else None
        )
        self.verification_level: int = data.get("verification_level", 0)
        self.default_message_notifications: int = data.get(
            "default_message_notifications", 0
        )
        self.explicit_content_filter: int = data.get("explicit_content_filter", 0)
        self.features: List[str] = data.get("features", [])
        self.mfa_level: int = data.get("mfa_level", 0)
        self.system_channel_id: Optional[int] = (
            int(data["system_channel_id"]) if data.get("system_channel_id") else None
        )
        self.system_channel_flags: int = data.get("system_channel_flags", 0)
        self.rules_channel_id: Optional[int] = (
            int(data["rules_channel_id"]) if data.get("rules_channel_id") else None
        )
        self.max_presences: Optional[int] = data.get("max_presences")
        self.max_members: Optional[int] = data.get("max_members")
        self.max_video_channel_users: Optional[int] = data.get(
            "max_video_channel_users"
        )
        self.vanity_url_code: Optional[str] = data.get("vanity_url_code")
        self.description: Optional[str] = data.get("description")
        self.banner: Optional[str] = data.get("banner")
        self.premium_tier: int = data.get("premium_tier", 0)
        self.premium_subscription_count: int = data.get(
            "premium_subscription_count", 0
        )
        self.preferred_locale: str = data.get("preferred_locale", "en-US")
        self.public_updates_channel_id: Optional[int] = (
            int(data["public_updates_channel_id"])
            if data.get("public_updates_channel_id")
            else None
        )
        self.safety_alerts_channel_id: Optional[int] = (
            int(data["safety_alerts_channel_id"])
            if data.get("safety_alerts_channel_id")
            else None
        )
        self.nsfw_level: int = data.get("nsfw_level", 0)

    @property
    def created_at(self) -> Optional[datetime]:
        try:
            return snowflake_time(self.id)
        except Exception:
            return None

    @property
    def icon_url(self) -> Optional[str]:
        if not self.icon:
            return None
        ext = "gif" if self.icon.startswith("a_") else "png"
        return f"https://cdn.discordapp.com/icons/{self.id}/{self.icon}.{ext}?size=1024"

    @property
    def banner_url(self) -> Optional[str]:
        if not self.banner:
            return None
        ext = "gif" if self.banner.startswith("a_") else "png"
        return f"https://cdn.discordapp.com/banners/{self.id}/{self.banner}.{ext}?size=1024"

    @property
    def splash_url(self) -> Optional[str]:
        if not self.splash:
            return None
        return f"https://cdn.discordapp.com/splashes/{self.id}/{self.splash}.png?size=1024"

    @property
    def discovery_splash_url(self) -> Optional[str]:
        if not self.discovery_splash:
            return None
        return f"https://cdn.discordapp.com/discovery-splashes/{self.id}/{self.discovery_splash}.png?size=1024"

    @property
    def vanity_url(self) -> Optional[str]:
        if not self.vanity_url_code:
            return None
        return f"https://discord.gg/{self.vanity_url_code}"

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"<Guild id={self.id} name='{self.name}'>"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Guild):
            return self.id == other.id
        return False

    def __hash__(self) -> int:
        return hash(self.id)
      
