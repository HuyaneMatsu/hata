import vampytest

from ....user import ClientUserBase, User, ZEROUSER

from ..subscription import Subscription

from .test__Subscription__constructor import _assert_fields_set


def test__Subscription__copy():
    """
    Tests whether ``Subscription.copy`` works as intended.
    """
    entitlement_ids = [202409220090, 202409220091]
    renewal_sku_ids = [202412210037, 202412210038]
    sku_ids = [202409220092, 202409220093]
    user_id = 202409220094
    
    subscription = Subscription(
        entitlement_ids = entitlement_ids,
        renewal_sku_ids = renewal_sku_ids,
        sku_ids = sku_ids,
        user_id = user_id,
    )
    
    copy = subscription.copy()
    _assert_fields_set(copy)
    vampytest.assert_eq(copy, subscription)
    vampytest.assert_not_is(copy, subscription)


def test__Subscription__copy_with__no_fields():
    """
    Tests whether ``Subscription.copy_with`` works as intended.
    
    Case: No parameters given.
    """
    entitlement_ids = [202409220095, 202409220096]
    renewal_sku_ids = [202412210039, 202412210040]
    sku_ids = [202409220097, 202409220098]
    user_id = 202409220099
    
    subscription = Subscription(
        entitlement_ids = entitlement_ids,
        renewal_sku_ids = renewal_sku_ids,
        sku_ids = sku_ids,
        user_id = user_id,
    )
    
    copy = subscription.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_eq(copy, subscription)
    vampytest.assert_not_is(copy, subscription)


def test__Subscription__copy_with__all_fields():
    """
    Tests whether ``Subscription.copy_with`` works as intended.
    
    Case: Stuffed.
    """
    old_entitlement_ids = [202409220100, 202409220101]
    old_renewal_sku_ids = [202412210041, 202412210042]
    old_sku_ids = [202409220102, 202409220103]
    old_user_id = 202409220104
    
    new_entitlement_ids = [202409220105, 202409220106]
    new_renewal_sku_ids = [202412210043, 202412210044]
    new_sku_ids = [202409220107, 202409220108]
    new_user_id = 202409220109
    
    
    subscription = Subscription(
        entitlement_ids = old_entitlement_ids,
        renewal_sku_ids = old_renewal_sku_ids,
        sku_ids = old_sku_ids,
        user_id = old_user_id,
    )
    
    copy = subscription.copy_with(
        entitlement_ids = new_entitlement_ids,
        renewal_sku_ids = new_renewal_sku_ids,
        sku_ids = new_sku_ids,
        user_id = new_user_id,
    )
    _assert_fields_set(copy)
    vampytest.assert_not_is(copy, subscription)

    vampytest.assert_eq(copy.entitlement_ids, tuple(new_entitlement_ids))
    vampytest.assert_eq(copy.renewal_sku_ids, tuple(new_renewal_sku_ids))
    vampytest.assert_eq(copy.sku_ids, tuple(new_sku_ids))
    vampytest.assert_eq(copy.user_id, new_user_id)


def test__Subscription__partial__true():
    """
    Tests whether ``Subscription.partial`` works as intended.
    
    Case: true.
    """
    subscription = Subscription()
    output = subscription.partial
    vampytest.assert_instance(output, bool)
    vampytest.assert_true(output)


def test__Subscription__partial__false():
    """
    Tests whether ``Subscription.partial`` works as intended.
    
    Case: false.
    """
    subscription_id = 202409220110
    
    subscription = Subscription.precreate(subscription_id)
    output = subscription.partial
    vampytest.assert_instance(output, bool)
    vampytest.assert_false(output)


def _iter_options__iter_entitlement_ids():
    entitlement_id_0 = 202409220111
    entitlement_id_1 = 202409220112
    
    yield None, []
    yield [entitlement_id_0], [entitlement_id_0]
    yield [entitlement_id_0, entitlement_id_1], [entitlement_id_0, entitlement_id_1]


@vampytest._(vampytest.call_from(_iter_options__iter_entitlement_ids()).returning_last())
def test__Subscription__iter_entitlement_ids(input_value):
    """
    Tests whether ``Subscription.iter_entitlement_ids`` works as intended.
    
    Parameters
    ----------
    input_value : `None | list<int>`
        Input value to create the instance with.
    
    Returns
    -------
    output : `list<int>`
    """
    subscription = Subscription(entitlement_ids = input_value)
    return [*subscription.iter_entitlement_ids()]


def _iter_options__iter_renewal_sku_ids():
    renewal_sku_id_0 = 202412210045
    renewal_sku_id_1 = 202412210046
    
    yield None, []
    yield [renewal_sku_id_0], [renewal_sku_id_0]
    yield [renewal_sku_id_0, renewal_sku_id_1], [renewal_sku_id_0, renewal_sku_id_1]


@vampytest._(vampytest.call_from(_iter_options__iter_renewal_sku_ids()).returning_last())
def test__Subscription__iter_renewal_sku_ids(input_value):
    """
    Tests whether ``Subscription.iter_renewal_sku_ids`` works as intended.
    
    Parameters
    ----------
    input_value : `None | list<int>`
        Input value to create the instance with.
    
    Returns
    -------
    output : `list<int>`
    """
    subscription = Subscription(renewal_sku_ids = input_value)
    return [*subscription.iter_renewal_sku_ids()]


def _iter_options__iter_sku_ids():
    sku_id_0 = 202409220113
    sku_id_1 = 202409220114
    
    yield None, []
    yield [sku_id_0], [sku_id_0]
    yield [sku_id_0, sku_id_1], [sku_id_0, sku_id_1]


@vampytest._(vampytest.call_from(_iter_options__iter_sku_ids()).returning_last())
def test__Subscription__iter_sku_ids(input_value):
    """
    Tests whether ``Subscription.iter_sku_ids`` works as intended.
    
    Parameters
    ----------
    input_value : `None | list<int>`
        Input value to create the instance with.
    
    Returns
    -------
    output : `list<int>`
    """
    subscription = Subscription(sku_ids = input_value)
    return [*subscription.iter_sku_ids()]


def _iter_options__user():
    user_id = 202409220115
    
    yield 0, ZEROUSER
    yield user_id, User.precreate(user_id)


@vampytest._(vampytest.call_from(_iter_options__user()).returning_last())
def test__Subscription__user(input_value):
    """
    Tests whether ``Subscription.user`` works as intended.
    
    Parameters
    ----------
    input_value : `None | int`
        Input value to create the instance with.
    
    Returns
    -------
    output : `ClientUserBase`
    """
    subscription = Subscription(user_id = input_value)
    output = subscription.user
    vampytest.assert_instance(output, ClientUserBase)
    return output


def _iter_options__sku_id():
    sku_id_0 = 202409240020
    sku_id_1 = 202409240021
    
    yield None, 0
    yield [sku_id_0], sku_id_0
    yield [sku_id_0, sku_id_1], sku_id_0


@vampytest._(vampytest.call_from(_iter_options__sku_id()).returning_last())
def test__Subscription__sku_id(input_value):
    """
    Tests whether ``Subscription.sku_id`` works as intended.
    
    Parameters
    ----------
    input_value : `None | list<int>`
        Input value to create the instance with.
    
    Returns
    -------
    output : `int`
    """
    subscription = Subscription(sku_ids = input_value)
    output = subscription.sku_id
    vampytest.assert_instance(output, int)
    return output
