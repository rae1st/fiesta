from __future__ import annotations
from typing import Optional, List, Dict, Any
from datetime import datetime
from ..utils import snowflake_time


class Channel:
    TYPES: Dict[int, str] = {
        0: "GUILD_TEXT",
        1: "DM",
        2: "GUILD_VOICE",
        3: "GROUP_DM",
        4: "GUILD_CATEGORY",
        5: "GUILD_NEWS",
        10: "NEWS_THREAD",
        11: "PUBLIC_THREAD",
        12: "PRIVATE_THREAD",
        13: "GUILD_STAGE_VOICE",
        14: "GUILD_DIRECTORY",
        15: "GUILD_FORUM",
        16: "GUILD_MEDIA",
    }

    def __init__(self, data: dict):
        self.id: int = int(data.get("id", 0))
        self.type: int = data.get("type", 0)
        self.guild_id: Optional[int] = (
            int(data["guild_id"]) if data.get("guild_id") else None
        )
        self.position: Optional[int] = data.get("position")
        self.name: str = data.get("name", "")
        self.topic: Optional[str] = data.get("topic")
        self.nsfw: bool = data.get("nsfw", False)
        self.last_message_id: Optional[int] = (
            int(data["last_message_id"]) if data.get("last_message_id") else None
        )
        self.bitrate: Optional[int] = data.get("bitrate")
        self.user_limit: Optional[int] = data.get("user_limit")
        self.rate_limit_per_user: int = data.get("rate_limit_per_user", 0)
        self.default_thread_rate_limit_per_user: Optional[int] = data.get(
            "default_thread_rate_limit_per_user"
        )
        self.icon: Optional[str] = data.get("icon")
        self.owner_id: Optional[int] = (
            int(data["owner_id"]) if data.get("owner_id") else None
        )
        self.application_id: Optional[int] = (
            int(data["application_id"]) if data.get("application_id") else None
        )
        self.parent_id: Optional[int] = (
            int(data["parent_id"]) if data.get("parent_id") else None
        )
        self.last_pin_timestamp: Optional[datetime] = (
            datetime.fromisoformat(data["last_pin_timestamp"].replace("Z", "+00:00"))
            if data.get("last_pin_timestamp")
            else None
        )
        self.rtc_region: Optional[str] = data.get("rtc_region")
        self.video_quality_mode: Optional[int] = data.get("video_quality_mode")
        self.message_count: Optional[int] = data.get("message_count")
        self.member_count: Optional[int] = data.get("member_count")
        self.default_auto_archive_duration: Optional[int] = data.get(
            "default_auto_archive_duration"
        )
        self.permissions: Optional[str] = data.get("permissions")
        self.flags: int = data.get("flags", 0)

        # Forum / media specific
        self.available_tags: List[Dict[str, Any]] = data.get("available_tags", [])
        self.applied_tags: List[int] = data.get("applied_tags", [])

    @property
    def created_at(self) -> Optional[datetime]:
        try:
            return snowflake_time(self.id)
        except Exception:
            return None

    @property
    def mention(self) -> str:
        return f"<#{self.id}>"

    @property
    def type_name(self) -> str:
        return self.TYPES.get(self.type, "UNKNOWN")

    @property
    def is_text(self) -> bool:
        return self.type in [0, 1, 3, 5, 10, 11, 12, 15, 16]

    @property
    def is_voice(self) -> bool:
        return self.type in [2, 13]

    @property
    def is_thread(self) -> bool:
        return self.type in [10, 11, 12]

    @property
    def is_dm(self) -> bool:
        return self.type in [1, 3]

    @property
    def is_nsfw(self) -> bool:
        return bool(self.nsfw)

    def __str__(self) -> str:
        return self.name or f"Channel {self.id}"

    def __repr__(self) -> str:
        return f"<Channel id={self.id} name='{self.name}' type={self.type_name}>"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Channel):
            return self.id == other.id
        return False

    def __hash__(self) -> int:
        return hash(self.id)
      
