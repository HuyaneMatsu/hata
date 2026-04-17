import vampytest

from ....application import Entitlement

from ...guild import Guild

from ..guild_enhancement_entitlements_create_event import GuildEnhancementEntitlementsCreateEvent

from .test__GuildEnhancementEntitlementsCreateEvent__constructor import _assert_fields_set


def test__GuildEnhancementEntitlementsCreateEvent__copy():
    """
    Tests whether ``GuildEnhancementEntitlementsCreateEvent.copy`` works as intended.
    """
    guild_id = 202507050026
    
    entitlements = [
        Entitlement.precreate(
            202507050027,
            guild_id = guild_id,
        ),
        Entitlement.precreate(
            202507050028,
            guild_id = guild_id,
        ),
    ]
    
    event = GuildEnhancementEntitlementsCreateEvent(
        entitlements = entitlements,
        guild_id = guild_id,
    )
    copy = event.copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(event, copy)

    vampytest.assert_eq(event, copy)



def test__GuildEnhancementEntitlementsCreateEvent__copy_with__no_fields():
    """
    Tests whether ``GuildEnhancementEntitlementsCreateEvent.copy_with`` works as intended.
    
    Case: no fields given.
    """
    guild_id = 202507050029
    
    entitlements = [
        Entitlement.precreate(
            202507050030,
            guild_id = guild_id,
        ),
        Entitlement.precreate(
            202507050031,
            guild_id = guild_id,
        ),
    ]
    
    event = GuildEnhancementEntitlementsCreateEvent(
        entitlements = entitlements,
        guild_id = guild_id,
    )
    copy = event.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_is_not(event, copy)

    vampytest.assert_eq(event, copy)



def test__GuildEnhancementEntitlementsCreateEvent__copy_with__all_fields():
    """
    Tests whether ``GuildEnhancementEntitlementsCreateEvent.copy_with`` works as intended.
    
    Case: all fields given.
    """
    old_guild_id = 202507050021
    
    old_entitlements = [
        Entitlement.precreate(
            202507050032,
            guild_id = old_guild_id,
        ),
        Entitlement.precreate(
            202507050033,
            guild_id = old_guild_id,
        ),
    ]
    
    new_guild_id = 202507050021
    
    new_entitlements = [
        Entitlement.precreate(
            202507050034,
            guild_id = new_guild_id,
        ),
        Entitlement.precreate(
            202507050035,
            guild_id = new_guild_id,
        ),
    ]
    
    event = GuildEnhancementEntitlementsCreateEvent(
        entitlements = old_entitlements,
        guild_id = old_guild_id,
    )
    copy = event.copy_with(
        entitlements = new_entitlements,
        guild_id = new_guild_id,
    )
    _assert_fields_set(copy)
    vampytest.assert_is_not(event, copy)

    vampytest.assert_eq(copy.guild_id, new_guild_id)
    vampytest.assert_eq(copy.entitlements, tuple(new_entitlements))


def _iter_options__guild():
    guild_id_0 = 202305160035
    guild_id_1 = 202305160036
    
    yield 0, None
    yield guild_id_0, None
    yield guild_id_1, Guild.precreate(guild_id_1)


@vampytest._(vampytest.call_from(_iter_options__guild()).returning_last())
def test__GuildEnhancementEntitlementsCreateEvent__guild(guild_id):
    """
    Tests whether ``GuildEnhancementEntitlementsCreateEvent.guild`` works as intended.
    
    Parameters
    ----------
    guild_id : `int`
        Guild identifier to create the event with.
    
    Returns
    -------
    guild : ``None | Guild``
    """
    event = GuildEnhancementEntitlementsCreateEvent(
        guild_id = guild_id,
    )
    
    output = event.guild
    vampytest.assert_instance(output, Guild, nullable = True)
    return output


def _iter_options__entitlement():
    guild_id = 202507050028
    
    entitlement_0 = Entitlement.precreate(
        202507050036,
        guild_id = guild_id,
    )
    
    entitlement_1 = Entitlement.precreate(
        202507050037,
        guild_id = guild_id,
    )
    
    yield None, None
    yield [entitlement_0], entitlement_0
    yield [entitlement_0, entitlement_1], entitlement_0


@vampytest._(vampytest.call_from(_iter_options__entitlement()).returning_last())
def test__GuildEnhancementEntitlementsCreateEvent__entitlement(entitlements):
    """
    Tests whether ``GuildEnhancementEntitlementsCreateEvent.entitlement`` works as intended.
    
    Parameters
    ----------
    entitlements : ``None | list<Entitlement>``
        Entitlements to create the event with.
    
    Returns
    -------
    entitlement : ``None | Entitlement``
    """
    event = GuildEnhancementEntitlementsCreateEvent(
        entitlements = entitlements,
    )
    
    output = event.entitlement
    vampytest.assert_instance(output, Entitlement, nullable = True)
    return output



def _iter_options__iter_entitlements():
    guild_id = 202507050028
    
    entitlement_0 = Entitlement.precreate(
        202507050036,
        guild_id = guild_id,
    )
    
    entitlement_1 = Entitlement.precreate(
        202507050037,
        guild_id = guild_id,
    )
    
    yield None, []
    yield [entitlement_0], [entitlement_0]
    yield [entitlement_0, entitlement_1], [entitlement_0, entitlement_1]


@vampytest._(vampytest.call_from(_iter_options__iter_entitlements()).returning_last())
def test__GuildEnhancementEntitlementsCreateEvent__iter_entitlements(entitlements):
    """
    Tests whether ``GuildEnhancementEntitlementsCreateEvent.iter_entitlements`` works as intended.
    
    Parameters
    ----------
    entitlements : ``None | list<Entitlement>``
        Entitlements to create the event with.
    
    Returns
    -------
    entitlement : ``list<Entitlement>``
    """
    event = GuildEnhancementEntitlementsCreateEvent(
        entitlements = entitlements,
    )
    
    output = [*event.iter_entitlements()]
    
    for element in output:
        vampytest.assert_instance(element, Entitlement)
    
    return output
