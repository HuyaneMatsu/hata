import vampytest

from ...message_role_subscription import MessageRoleSubscription

from ..fields import parse_role_subscription


def _iter_options():
    message_role_subscription = MessageRoleSubscription(
        tier_name = 'hell',
    )
    
    yield (
        {},
        None,
    )
    
    yield (
        {
            'role_subscription_data': None,
        },
        None,
    )
    
    yield (
        {
            'role_subscription_data': message_role_subscription.to_data(),
        },
        message_role_subscription,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_role_subscription(input_data):
    """
    Tests whether ``parse_role_subscription`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : ``None | MessageRoleSubscription``
    """
    output = parse_role_subscription(input_data)
    vampytest.assert_instance(output, MessageRoleSubscription, nullable = True)
    return output
