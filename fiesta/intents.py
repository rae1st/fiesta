from __future__ import annotations


class Intents:
    """Discord Gateway Intents (2025 ready)."""

    # Intents bit values (from Discord docs)
    GUILDS = 1 << 0
    GUILD_MEMBERS = 1 << 1
    GUILD_MODERATION = 1 << 2
    GUILD_EMOJIS_AND_STICKERS = 1 << 3
    GUILD_INTEGRATIONS = 1 << 4
    GUILD_WEBHOOKS = 1 << 5
    GUILD_INVITES = 1 << 6
    GUILD_VOICE_STATES = 1 << 7
    GUILD_PRESENCES = 1 << 8
    GUILD_MESSAGES = 1 << 9
    GUILD_MESSAGE_REACTIONS = 1 << 10
    GUILD_MESSAGE_TYPING = 1 << 11
    DIRECT_MESSAGES = 1 << 12
    DIRECT_MESSAGE_REACTIONS = 1 << 13
    DIRECT_MESSAGE_TYPING = 1 << 14
    MESSAGE_CONTENT = 1 << 15

    def __init__(self, value: int = 0):
        self.value: int = value

    # ----------------------------
    # Factory methods
    # ----------------------------
    @classmethod
    def none(cls) -> Intents:
        """No intents enabled."""
        return cls(0)

    @classmethod
    def default(cls) -> Intents:
        """Default intents for most bots (excludes presence & message_content)."""
        return cls(
            cls.GUILDS
            | cls.GUILD_MEMBERS
            | cls.GUILD_MODERATION
            | cls.GUILD_EMOJIS_AND_STICKERS
            | cls.GUILD_INTEGRATIONS
            | cls.GUILD_WEBHOOKS
            | cls.GUILD_INVITES
            | cls.GUILD_VOICE_STATES
            | cls.GUILD_MESSAGES
            | cls.GUILD_MESSAGE_REACTIONS
            | cls.DIRECT_MESSAGES
            | cls.DIRECT_MESSAGE_REACTIONS
        )

    @classmethod
    def all(cls) -> Intents:
        """All possible intents (requires verification for large bots)."""
        return cls(
            cls.GUILDS
            | cls.GUILD_MEMBERS
            | cls.GUILD_MODERATION
            | cls.GUILD_EMOJIS_AND_STICKERS
            | cls.GUILD_INTEGRATIONS
            | cls.GUILD_WEBHOOKS
            | cls.GUILD_INVITES
            | cls.GUILD_VOICE_STATES
            | cls.GUILD_PRESENCES
            | cls.GUILD_MESSAGES
            | cls.GUILD_MESSAGE_REACTIONS
            | cls.GUILD_MESSAGE_TYPING
            | cls.DIRECT_MESSAGES
            | cls.DIRECT_MESSAGE_REACTIONS
            | cls.DIRECT_MESSAGE_TYPING
            | cls.MESSAGE_CONTENT
        )

    @classmethod
    def from_value(cls, value: int) -> Intents:
        """Create intents object from raw bit value."""
        return cls(value)

    # ----------------------------
    # Helpers
    # ----------------------------
    def has(self, flag: int) -> bool:
        """Check if an intent is enabled."""
        return (self.value & flag) == flag

    def enable(self, flag: int) -> None:
        """Enable a specific intent."""
        self.value |= flag

    def disable(self, flag: int) -> None:
        """Disable a specific intent."""
        self.value &= ~flag

    # ----------------------------
    # Operators
    # ----------------------------
    def __or__(self, other: Intents) -> Intents:
        return Intents(self.value | other.value)

    def __and__(self, other: Intents) -> Intents:
        return Intents(self.value & other.value)

    def __contains__(self, flag: int) -> bool:
        return self.has(flag)

    # ----------------------------
    # Debugging / display
    # ----------------------------
    def __repr__(self) -> str:
        return f"<Intents value={self.value}>"
      
