from typing import List, Optional
from datetime import datetime
from ..utils import snowflake_time, clean_content
from .user import User


class Message:
    TYPES = {
        0: "DEFAULT",
        1: "RECIPIENT_ADD",
        2: "RECIPIENT_REMOVE",
        3: "CALL",
        4: "CHANNEL_NAME_CHANGE",
        5: "CHANNEL_ICON_CHANGE",
        6: "CHANNEL_PINNED_MESSAGE",
        7: "USER_JOIN",
        8: "GUILD_BOOST",
        9: "GUILD_BOOST_TIER_1",
        10: "GUILD_BOOST_TIER_2",
        11: "GUILD_BOOST_TIER_3",
        12: "CHANNEL_FOLLOW_ADD",
        19: "REPLY",
        20: "CHAT_INPUT_COMMAND",
        21: "THREAD_STARTER_MESSAGE",
        22: "GUILD_INVITE_REMINDER",
        23: "CONTEXT_MENU_COMMAND",
        24: "AUTO_MODERATION_ACTION",
        25: "ROLE_SUBSCRIPTION_PURCHASE",
    }

    def __init__(self, data: dict):
        self.id = int(data.get("id", 0))
        self.channel_id = int(data.get("channel_id", 0))
        self.guild_id = data.get("guild_id")
        self.author = User(data.get("author", {})) if data.get("author") else None
        self.content = data.get("content", "")
        self.timestamp = data.get("timestamp")
        self.edited_timestamp = data.get("edited_timestamp")
        self.tts = data.get("tts", False)
        self.mention_everyone = data.get("mention_everyone", False)
        self.mentions = [User(user) for user in data.get("mentions", [])]
        self.mention_roles = data.get("mention_roles", [])
        self.mention_channels = data.get("mention_channels", [])
        self.attachments = data.get("attachments", [])
        self.embeds = data.get("embeds", [])
        self.reactions = data.get("reactions", [])
        self.nonce = data.get("nonce")
        self.pinned = data.get("pinned", False)
        self.webhook_id = data.get("webhook_id")
        self.type = data.get("type", 0)
        self.activity = data.get("activity")
        self.application = data.get("application")
        self.application_id = data.get("application_id")
        self.message_reference = data.get("message_reference")
        self.flags = data.get("flags", 0)
        self.referenced_message = data.get("referenced_message")
        self.interaction = data.get("interaction")
        self.thread = data.get("thread")
        self.components = data.get("components", [])
        self.sticker_items = data.get("sticker_items", [])
        self.position = data.get("position")
        self.role_subscription_data = data.get("role_subscription_data")

    @property
    def created_at(self) -> datetime:
        return snowflake_time(self.id)

    @property
    def edited_at(self) -> Optional[datetime]:
        if not self.edited_timestamp:
            return None
        return datetime.fromisoformat(self.edited_timestamp.replace("Z", "+00:00"))

    @property
    def clean_content(self) -> str:
        return clean_content(self.content)

    @property
    def jump_url(self) -> str:
        guild_part = "@me" if not self.guild_id else str(self.guild_id)
        return f"https://discord.com/channels/{guild_part}/{self.channel_id}/{self.id}"

    @property
    def type_name(self) -> str:
        return self.TYPES.get(self.type, "UNKNOWN")

    @property
    def is_system(self) -> bool:
        return self.type != 0

    @property
    def has_attachments(self) -> bool:
        return len(self.attachments) > 0

    @property
    def has_embeds(self) -> bool:
        return len(self.embeds) > 0

    @property
    def is_reply(self) -> bool:
        return self.message_reference is not None

    def __str__(self) -> str:
        return self.content

    def __repr__(self) -> str:
        return f"<Message id={self.id} author='{self.author.username if self.author else 'Unknown'}' channel_id={self.channel_id}>"
  
