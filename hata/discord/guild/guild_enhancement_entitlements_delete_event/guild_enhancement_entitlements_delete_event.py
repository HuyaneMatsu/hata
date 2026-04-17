__all__ = ('GuildEnhancementEntitlementsDeleteEvent',)


from ..guild_enhancement_entitlements_create_event import GuildEnhancementEntitlementsCreateEvent

class GuildEnhancementEntitlementsDeleteEvent(GuildEnhancementEntitlementsCreateEvent):
    """
    Represents a `GUILD_POWERUP_ENTITLEMENTS_DELETE` event.
    
    Attributes
    ----------
    entitlements : ``None | tuple<Entitlement>``
        The affected entitlements.
    
    guild_id : `int`
        The guild's identifier where the event is for.
    """
    __slots__ = ()
