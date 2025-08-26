from __future__ import annotations
import re
from datetime import datetime, timezone
from enum import IntEnum
from typing import Optional


def snowflake_time(snowflake: int) -> datetime:
    """Extract timestamp from Discord snowflake"""
    timestamp = ((snowflake >> 22) + 1420070400000) / 1000
    return datetime.fromtimestamp(timestamp, tz=timezone.utc)


def parse_mention(content: str) -> Optional[int]:
    """Extract user ID from mention string"""
    match = re.search(r"<@!?(\d+)>", content)
    return int(match.group(1)) if match else None


def parse_channel_mention(content: str) -> Optional[int]:
    """Extract channel ID from channel mention"""
    match = re.search(r"<#(\d+)>", content)
    return int(match.group(1)) if match else None


def parse_role_mention(content: str) -> Optional[int]:
    """Extract role ID from role mention"""
    match = re.search(r"<@&(\d+)>", content)
    return int(match.group(1)) if match else None


def escape_markdown(text: str) -> str:
    """Escape Discord markdown characters"""
    return re.sub(r"([*_`~|\\])", r"\\\1", text)


def clean_content(content: str) -> str:
    """Clean message content (remove mentions, etc.)"""
    content = re.sub(r"<@!?(\d+)>", "@user", content)
    content = re.sub(r"<#(\d+)>", "#channel", content)
    content = re.sub(r"<@&(\d+)>", "@role", content)
    return content


class Color(IntEnum):
    """Discord embed colors"""

    RED = 0xFF0000
    GREEN = 0x00FF00
    BLUE = 0x0000FF
    YELLOW = 0xFFFF00
    PURPLE = 0x800080
    ORANGE = 0xFFA500
    PINK = 0xFFC0CB
    CYAN = 0x00FFFF
    BLACK = 0x000000
    WHITE = 0xFFFFFF
    DISCORD_BLURPLE = 0x5865F2
    DISCORD_GREEN = 0x57F287
    DISCORD_YELLOW = 0xFEE75C
    DISCORD_FUCHSIA = 0xEB459E
    DISCORD_RED = 0xED4245


def create_embed(
    title: str | None = None,
    description: str | None = None,
    color: int = Color.DISCORD_BLURPLE,
    url: str | None = None,
    thumbnail: str | None = None,
    image: str | None = None,
    timestamp: datetime | None = None,
    fields: list[dict[str, str | bool]] | None = None,
) -> dict:
    """Create Discord embed object"""
    embed: dict[str, object] = {"color": int(color)}

    if title:
        embed["title"] = title
    if description:
        embed["description"] = description
    if url:
        embed["url"] = url
    if thumbnail:
        embed["thumbnail"] = {"url": thumbnail}
    if image:
        embed["image"] = {"url": image}
    if timestamp:
        embed["timestamp"] = timestamp.astimezone(timezone.utc).isoformat()
    if fields:
        embed["fields"] = fields

    return embed
  
