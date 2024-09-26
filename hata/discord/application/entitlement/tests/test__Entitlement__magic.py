from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ..entitlement import Entitlement
from ..preinstanced import EntitlementType


def test__Entitlement__repr():
    """
    Tests whether ``Entitlement.__repr__`` works as intended.
    
    Case: include defaults and internals.
    """
    entitlement_id = 202310040036
    application_id = 202310040037
    consumed = True
    deleted = True
    ends_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    entitlement_type = EntitlementType.user_gift
    guild_id = 202310040038
    sku_id = 202310040039
    starts_at = DateTime(2015, 5, 14, tzinfo = TimeZone.utc)
    subscription_id = 202310040040
    user_id = 202310040041
    
    entitlement = Entitlement.precreate(
        entitlement_id,
        application_id = application_id,
        consumed = consumed,
        deleted = deleted,
        ends_at = ends_at,
        entitlement_type = entitlement_type,
        guild_id = guild_id,
        sku_id = sku_id,
        starts_at = starts_at,
        subscription_id = subscription_id,
        user_id = user_id,
    )
    
    vampytest.assert_instance(repr(entitlement), str)


def test__Entitlement__hash():
    """
    Tests whether ``Entitlement.__hash__`` works as intended.
    
    Case: include defaults and internals.
    """
    entitlement_id = 202310040042
    application_id = 202310040043
    consumed = True
    deleted = True
    ends_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    entitlement_type = EntitlementType.user_gift
    guild_id = 202310040044
    sku_id = 202310040045
    starts_at = DateTime(2015, 5, 14, tzinfo = TimeZone.utc)
    subscription_id = 202310040046
    user_id = 202310040047
    
    keyword_parameters = {
        'guild_id': guild_id,
        'sku_id': sku_id,
        'user_id': user_id,
    }
    
    # Full
    entitlement = Entitlement.precreate(
        entitlement_id,
        application_id = application_id,
        consumed = consumed,
        deleted = deleted,
        ends_at = ends_at,
        entitlement_type = entitlement_type,
        starts_at = starts_at,
        subscription_id = subscription_id,
        **keyword_parameters,
    )
    
    vampytest.assert_instance(hash(entitlement), int)
    
    # Partial
    entitlement = Entitlement(**keyword_parameters,)
    
    vampytest.assert_instance(hash(entitlement), int)


def _iter_options__eq__partial():
    guild_id = 202409220020
    sku_id = 202409220021
    user_id = 202409220022
    
    keyword_parameters = {
        'guild_id': guild_id,
        'sku_id': sku_id,
        'user_id': user_id,
    }
    
    yield (
        {},
        {},
        True,
    )
    
    yield (
        keyword_parameters,
        keyword_parameters,
        True,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'guild_id': 202409220023,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'sku_id': 202409220024,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'user_id': 202409220025,
        },
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq__partial()).returning_last())
def test__Entitlement__eq__partial(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``Entitlement.__eq__`` works as intended.
    
    Case: partial
    
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
    entitlement_0 = Entitlement(**keyword_parameters_0)
    entitlement_1 = Entitlement(**keyword_parameters_1)
    
    output = entitlement_0 == entitlement_1
    vampytest.assert_instance(output, bool)
    return output


def test__Entitlement__eq():
    """
    Tests whether ``Entitlement.__eq__`` works as intended.
    
    Case: include defaults and internals.
    """
    entitlement_id_0 = 202409220026
    entitlement_id_1 = 202409220027
    guild_id_0 = 202409220028
    guild_id_1 = 202409220029
    
    entitlement_0 = Entitlement.precreate(
        entitlement_id_0,
        guild_id = guild_id_0,
    )
    
    entitlement_1 = Entitlement.precreate(
        entitlement_id_1,
        guild_id = guild_id_1,
    )
    
    entitlement_2 = Entitlement(
        guild_id = guild_id_0
    )
    
    vampytest.assert_eq(entitlement_0, entitlement_0)
    vampytest.assert_ne(entitlement_0, entitlement_1)
    vampytest.assert_ne(entitlement_1, entitlement_2)
    vampytest.assert_eq(entitlement_0, entitlement_2)
    vampytest.assert_ne(entitlement_0, object())
