from datetime import datetime as DateTime

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
    ends_at = DateTime(2016, 5, 14)
    entitlement_type = EntitlementType.user_gift
    guild_id = 202310040038
    sku_id = 202310040039
    starts_at = DateTime(2015, 5, 14)
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
    ends_at = DateTime(2016, 5, 14)
    entitlement_type = EntitlementType.user_gift
    guild_id = 202310040044
    sku_id = 202310040045
    starts_at = DateTime(2015, 5, 14)
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


def test__Entitlement__eq():
    """
    Tests whether ``Entitlement.__eq__`` works as intended.
    
    Case: include defaults and internals.
    """
    entitlement_id = 202310040048
    application_id = 202310040049
    consumed = True
    deleted = True
    ends_at = DateTime(2016, 5, 14)
    entitlement_type = EntitlementType.user_gift
    guild_id = 202310040050
    sku_id = 202310040051
    starts_at = DateTime(2015, 5, 14)
    subscription_id = 202310040052
    user_id = 202310040053
    
    keyword_parameters = {
        'guild_id': guild_id,
        'sku_id': sku_id,
        'user_id': user_id,
    }
    
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
    
    vampytest.assert_eq(entitlement, entitlement)
    vampytest.assert_ne(entitlement, object())
    
    test_entitlement = Entitlement(**keyword_parameters)
    vampytest.assert_eq(entitlement, test_entitlement)
    
    for field_name, field_value in (
        ('guild_id', 202310040054),
        ('sku_id', 202310040055),
        ('user_id', 202310040056),
    ):
        test_entitlement = Entitlement(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(entitlement, test_entitlement)
