import vampytest

from ....application import Entitlement

from ..guild_enhancement_entitlements_create_event import GuildEnhancementEntitlementsCreateEvent


def _assert_fields_set(event):
    """
    Checks whether every attribute is set of the given guild join request delete event.
    
    Parameters
    ----------
    event : ``GuildEnhancementEntitlementsCreateEvent``
        The event to check.
    """
    vampytest.assert_instance(event, GuildEnhancementEntitlementsCreateEvent)
    vampytest.assert_instance(event.entitlements, tuple, nullable = True)
    vampytest.assert_instance(event.guild_id, int)


def test__GuildEnhancementEntitlementsCreateEvent__new__no_fields():
    """
    Tests whether ``GuildEnhancementEntitlementsCreateEvent.__new__`` works as intended.
    
    Case: No fields given.
    """
    event = GuildEnhancementEntitlementsCreateEvent()
    _assert_fields_set(event)


def test__GuildEnhancementEntitlementsCreateEvent__new__all_fields():
    """
    Tests whether ``GuildEnhancementEntitlementsCreateEvent.__new__`` works as intended.
    
    Case: Fields given.
    """
    guild_id = 202507050008
    
    entitlements = [
        Entitlement.precreate(
            202507050006,
            guild_id = guild_id,
        ),
        Entitlement.precreate(
            202507050007,
            guild_id = guild_id,
        ),
    ]
    
    event = GuildEnhancementEntitlementsCreateEvent(
        entitlements = entitlements,
        guild_id = guild_id,
    )
    _assert_fields_set(event)
    
    vampytest.assert_eq(event.entitlements, tuple(entitlements))
    vampytest.assert_eq(event.guild_id, guild_id)
