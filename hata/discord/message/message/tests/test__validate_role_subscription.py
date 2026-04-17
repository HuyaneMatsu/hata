import vampytest

from ...message_role_subscription import MessageRoleSubscription


from ..fields import validate_role_subscription


def _iter_options__passing():
    message_role_subscription = MessageRoleSubscription(
        tier_name = 'hell',
    )
    
    yield (
        None,
        None,
    )
    
    yield (
        message_role_subscription,
        message_role_subscription,
    )


def _iter_options__type_error():
    yield 12.6


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_role_subscription(input_value):
    """
    Tests whether ``validate_role_subscription`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        The value to validate.
    
    Returns
    -------
    output : ``None | MessageRoleSubscription``
    
    Raises
    ------
    TypeError
    """
    output = validate_role_subscription(input_value)
    vampytest.assert_instance(output, MessageRoleSubscription, nullable = True)
    return output
