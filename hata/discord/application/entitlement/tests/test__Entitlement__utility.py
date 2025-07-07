import vampytest

from ...sku import SKU

from ..entitlement import Entitlement
from ..preinstanced import EntitlementOwnerType

from .test__Entitlement__constructor import _assert_fields_set


def test__Entitlement__copy():
    """
    Tests whether ``Entitlement.copy`` works as intended.
    """
    guild_id = 202310040057
    sku_id = 202310040058
    user_id = 202310040059
    
    entitlement = Entitlement(
        guild_id = guild_id,
        sku_id = sku_id,
        user_id = user_id,
    )
    
    copy = entitlement.copy()
    _assert_fields_set(copy)
    vampytest.assert_eq(copy, entitlement)
    vampytest.assert_not_is(copy, entitlement)


def test__Entitlement__copy_with__no_fields():
    """
    Tests whether ``Entitlement.copy_with`` works as intended.
    
    Case: No parameters given.
    """
    guild_id = 202310040060
    sku_id = 202310040061
    user_id = 202310040062
    
    entitlement = Entitlement(
        guild_id = guild_id,
        sku_id = sku_id,
        user_id = user_id,
    )
    
    copy = entitlement.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_eq(copy, entitlement)
    vampytest.assert_not_is(copy, entitlement)


def test__Entitlement__copy_with__all_fields():
    """
    Tests whether ``Entitlement.copy_with`` works as intended.
    
    Case: Stuffed.
    """
    old_guild_id = 202310040063
    old_sku_id = 202310040064
    old_user_id = 202310040065
    
    new_guild_id = 202310040066
    new_sku_id = 202310040067
    new_user_id = 202310040068
    
    
    entitlement = Entitlement(
        guild_id = old_guild_id,
        sku_id = old_sku_id,
        user_id = old_user_id,
    )
    
    copy = entitlement.copy_with(
        guild_id = new_guild_id,
        sku_id = new_sku_id,
        user_id = new_user_id,
    )
    _assert_fields_set(copy)
    vampytest.assert_not_is(copy, entitlement)

    vampytest.assert_eq(copy.guild_id, new_guild_id)
    vampytest.assert_eq(copy.sku_id, new_sku_id)
    vampytest.assert_eq(copy.user_id, new_user_id)


def test__Entitlement__partial__true():
    """
    Tests whether ``Entitlement.partial`` works as intended.
    
    Case: true.
    """
    entitlement = Entitlement()
    output = entitlement.partial
    vampytest.assert_instance(output, bool)
    vampytest.assert_true(output)


def test__Entitlement__partial__false():
    """
    Tests whether ``Entitlement.partial`` works as intended.
    
    Case: false.
    """
    entitlement_id = 202310040069
    
    entitlement = Entitlement.precreate(entitlement_id)
    output = entitlement.partial
    vampytest.assert_instance(output, bool)
    vampytest.assert_false(output)


def _iter_options__owner_id():
    guild_id = 202310040070
    user_id = 202310040071
    
    yield 202507040003, {}, 0
    yield 202507040004, {'guild_id': guild_id}, guild_id
    yield 202507040005, {'user_id': user_id}, user_id
    
    
@vampytest._(vampytest.call_from(_iter_options__owner_id()).returning_last())
def test__Entitlement__owner_id(entitlement_id, keyword_parameters):
    """
    Tests whether ``Entitlement.owner_id`` works as intended.
    
    Parameters
    ----------
    entitlement_id : `int`.
        Entitlement identifier.
    
    Keyword_parameters : `dict<str, object>`
        Keyword parameters to create entitlement with.
    
    Returns
    -------
    output : `int`
    """
    entitlement = Entitlement.precreate(entitlement_id, **keyword_parameters)
    output = entitlement.owner_id
    vampytest.assert_instance(output, int)
    return output


def _iter_options__owner_type():
    guild_id = 202310040072
    user_id = 202310040073
    
    yield 202507040006, {}, 0
    yield 202507040007, {'guild_id': guild_id}, EntitlementOwnerType.guild
    yield 202507040008, {'user_id': user_id}, EntitlementOwnerType.user
    
    
@vampytest._(vampytest.call_from(_iter_options__owner_type()).returning_last())
def test__Entitlement__owner_type(entitlement_id, keyword_parameters):
    """
    Tests whether ``Entitlement.owner_type`` works as intended.
    
    Parameters
    ----------
    entitlement_id : `int`.
        Entitlement identifier.
    
    Keyword_parameters : `dict<str, object>`
        Keyword parameters to create entitlement with.
    
    Returns
    -------
    output : ``EntitlementOwnerType``
    """
    entitlement = Entitlement.precreate(entitlement_id, **keyword_parameters)
    output = entitlement.owner_type
    vampytest.assert_instance(output, EntitlementOwnerType)
    return output


def _iter_options__sku():
    sku_id_0 = 202507040009
    sku_id_1 = 202507040010
    
    sku_1 = SKU.precreate(
        sku_id_1,
    )
    
    yield 202507040011, 0, None, (None, None)
    yield 202507040012, sku_id_0, None, (None, None)
    yield 202507040013, sku_id_1, None, (sku_1, sku_1)
    yield 202507040014, sku_id_1, sku_1, (sku_1, sku_1)


@vampytest._(vampytest.call_from(_iter_options__sku()).returning_last())
def test__Entitlement__sku(entitlement_id, sku_id, sku):
    """
    Tests whether ``Entitlement.sku`` works as intended.
    
    Parameters
    ----------
    entitlement_id : `int`.
        Entitlement identifier.
    
    sku_id : `int`
        Stock keeping unit identifier.
    
    sku : ``None | SKU``
        Stock keeping unit to create the entitlement with.
    
    Returns
    -------
    output : ``(None | SKU, None | SKU)``
    """
    entitlement = Entitlement.precreate(entitlement_id, sku_id = sku_id, sku = sku)
    output = entitlement.sku
    vampytest.assert_instance(output, SKU, nullable = True)
    return (output, entitlement._sku)
