from __future__ import annotations
from typing import TYPE_CHECKING, Any
from ..models import User, Channel, Guild, Message
from ..utils import create_embed

if TYPE_CHECKING:
    from ..client import Client


class Context:
    """Command execution context"""

    def __init__(self, client: Client, data: dict[str, Any]):
        self.client = client
        self._data = data

        self.guild_id: str | None = data.get("guild_id")
        self.channel_id: str | None = data.get("channel_id")
        self.message_id: str | None = data.get("id")

        self.author = User(data.get("author", {}))
        self.channel = Channel({"id": self.channel_id, "type": 0})
        self.guild = Guild({"id": self.guild_id}) if self.guild_id else None
        self.message = Message(data)

        self.prefix: str = client.command_prefix
        self.content: str = data.get("content", "")
        if self.content.startswith(self.prefix):
            parts = self.content[len(self.prefix) :].split()
            self.args = parts[1:] if len(parts) > 1 else []
        else:
            self.args: list[str] = []

    async def send(
        self,
        content: str | None = None,
        *,
        embed: dict[str, Any] | None = None,
        embeds: list[dict[str, Any]] | None = None,
        components: list[dict[str, Any]] | None = None,
        ephemeral: bool = False,
    ) -> dict[str, Any]:
        return await self.client._http.send_message(
            self.channel_id,
            content=content,
            embeds=embeds or ([embed] if embed else None),
            components=components,
        )

    async def reply(
        self,
        content: str | None = None,
        *,
        embed: dict[str, Any] | None = None,
        embeds: list[dict[str, Any]] | None = None,
        mention_author: bool = True,
    ) -> dict[str, Any]:
        if mention_author and content:
            content = f"<@{self.author.id}> {content}"
        return await self.send(content=content, embed=embed, embeds=embeds)

    async def send_embed(
        self,
        title: str | None = None,
        description: str | None = None,
        color: int = 0x5865F2,
        **kwargs: Any,
    ) -> dict[str, Any]:
        embed = create_embed(title=title, description=description, color=color, **kwargs)
        return await self.send(embed=embed)

    @property
    def clean_content(self) -> str:
        from ..utils import clean_content
        return clean_content(self.content)

    def typing(self) -> TypingContext:
        return TypingContext(self)


class TypingContext:
    """Typing indicator context manager"""

    def __init__(self, ctx: Context):
        self.ctx = ctx

    async def __aenter__(self):
        # TODO: implement Discord typing endpoint
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        return False
