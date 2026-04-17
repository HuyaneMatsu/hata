import vampytest

from ....application import Entitlement

from ..guild_enhancement_entitlements_create_event import GuildEnhancementEntitlementsCreateEvent

from .test__GuildEnhancementEntitlementsCreateEvent__constructor import _assert_fields_set


def test__GuildEnhancementEntitlementsCreateEvent__from_data():
    """
    Tests whether ``GuildEnhancementEntitlementsCreateEvent.from_data`` works as intended.
    
    Case: all fields given.
    """
    guild_id = 202507050009
    
    entitlements = [
        Entitlement.precreate(
            202507050010,
            guild_id = guild_id,
        ),
        Entitlement.precreate(
            202507050011,
            guild_id = guild_id,
        ),
    ]
    
    data = {
        'entitlements': [entitlement.to_data(include_internals = True) for entitlement in entitlements],
        'guild_id': str(guild_id),
    }
    
    event = GuildEnhancementEntitlementsCreateEvent.from_data(data)
    _assert_fields_set(event)
    
    vampytest.assert_eq(event.entitlements, tuple(entitlements))
    vampytest.assert_eq(event.guild_id, guild_id)


def test__GuildEnhancementEntitlementsCreateEvent__to_data():
    """
    Tests whether ``GuildEnhancementEntitlementsCreateEvent.to_data`` works as intended.
    
    Case: Include defaults.
    """
    guild_id = 202507050012
    
    entitlements = [
        Entitlement.precreate(
            202507050013,
            guild_id = guild_id,
        ),
        Entitlement.precreate(
            202507050014,
            guild_id = guild_id,
        ),
    ]
    
    event = GuildEnhancementEntitlementsCreateEvent(
        entitlements = entitlements,
        guild_id = guild_id,
    )
    
    expected_output = {
        'entitlements': [
            entitlement.to_data(defaults = True, include_internals = True)
            for entitlement in entitlements
        ],
        'guild_id': str(guild_id),
    }
    
    vampytest.assert_eq(
        event.to_data(defaults = True),
        expected_output,
    )
