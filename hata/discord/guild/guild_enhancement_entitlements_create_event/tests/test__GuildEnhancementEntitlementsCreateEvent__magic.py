import vampytest

from ....application import Entitlement

from ..guild_enhancement_entitlements_create_event import GuildEnhancementEntitlementsCreateEvent


def test__GuildEnhancementEntitlementsCreateEvent__repr():
    """
    Tests whether ``GuildEnhancementEntitlementsCreateEvent.__repr__`` works as intended.
    """
    guild_id = 202507050015
    
    entitlements = [
        Entitlement.precreate(
            202507050016,
            guild_id = guild_id,
        ),
        Entitlement.precreate(
            202507050017,
            guild_id = guild_id,
        ),
    ]
    
    event = GuildEnhancementEntitlementsCreateEvent(
        entitlements = entitlements,
        guild_id = guild_id,
    )
    
    vampytest.assert_instance(repr(event), str)


def test__GuildEnhancementEntitlementsCreateEvent__hash():
    """
    Tests whether ``GuildEnhancementEntitlementsCreateEvent.__hash__`` works as intended.
    """
    guild_id = 202507050018
    
    entitlements = [
        Entitlement.precreate(
            202507050019,
            guild_id = guild_id,
        ),
        Entitlement.precreate(
            202507050020,
            guild_id = guild_id,
        ),
    ]
    
    event = GuildEnhancementEntitlementsCreateEvent(
        entitlements = entitlements,
        guild_id = guild_id,
    )
    
    vampytest.assert_instance(hash(event), int)


def _iter_options__eq():
    guild_id = 202507050021
    
    entitlements = [
        Entitlement.precreate(
            202507050022,
            guild_id = guild_id,
        ),
        Entitlement.precreate(
            202507050023,
            guild_id = guild_id,
        ),
    ]
    
    keyword_parameters = {
        'entitlements': entitlements,
        'guild_id': guild_id,
    }
    
    yield (
        keyword_parameters,
        keyword_parameters,
        True,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'entitlements': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'guild_id': 0,
        },
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__GuildEnhancementEntitlementsCreateEvent__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``GuildEnhancementEntitlementsCreateEvent.__eq__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters_0 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    keyword_parameters_1 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : `bool`
    """
    event_0 = GuildEnhancementEntitlementsCreateEvent(**keyword_parameters_0)
    event_1 = GuildEnhancementEntitlementsCreateEvent(**keyword_parameters_1)
    
    output = event_0 == event_1
    vampytest.assert_instance(output, bool)
    return output


def test__GuildEnhancementEntitlementsCreateEvent__unpack():
    """
    Tests whether ``GuildEnhancementEntitlementsCreateEvent`` unpacking works as intended.
    """
    guild_id = 202507050024
    
    entitlements = [
        Entitlement.precreate(
            202507050025,
            guild_id = guild_id,
        ),
        Entitlement.precreate(
            202507050026,
            guild_id = guild_id,
        ),
    ]
    
    event = GuildEnhancementEntitlementsCreateEvent(
        entitlements = entitlements,
        guild_id = guild_id,
    )
    
    vampytest.assert_eq(len([*event]), len(event))
