import vampytest

from ...message_role_subscription import MessageRoleSubscription

from ..fields import put_role_subscription


def _iter_options():
    message_role_subscription = MessageRoleSubscription(
        tier_name = 'hell',
    )
    
    yield (
        None,
        False,
        {},
    )
    
    yield (
        None,
        True,
        {
            'role_subscription_data': None,
        },
    )
    
    yield (
        message_role_subscription,
        False,
        {
            'role_subscription_data': message_role_subscription.to_data(defaults = False),
        },
    )
    
    yield (
        message_role_subscription,
        True,
        {
            'role_subscription_data': message_role_subscription.to_data(defaults = True),
        },
    )

@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_role_subscription(input_value, defaults):
    """
    Tests whether ``put_role_subscription`` is working as intended.
    
    Parameters
    ----------
    input_value : ``None | MessageRoleSubscription``
        The value to serialize.
    
    defaults : `bool`
        Whether values as their default should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_role_subscription(input_value, {}, defaults)
