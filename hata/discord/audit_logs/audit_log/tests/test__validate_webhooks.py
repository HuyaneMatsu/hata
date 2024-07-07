import vampytest

from ....webhook import Webhook

from ..fields import validate_webhooks


def _iter_options__passing():
    webhook_id_0 = 202406270002
    webhook_id_1 = 202406270003
    
    webhook_0 = Webhook.precreate(webhook_id_0)
    webhook_1 = Webhook.precreate(webhook_id_1)

    yield None, None
    yield [], None
    yield [webhook_0], {webhook_id_0: webhook_0}
    yield [webhook_0, webhook_0], {webhook_id_0: webhook_0}
    yield [webhook_1, webhook_0], {webhook_id_0: webhook_0, webhook_id_1: webhook_1}



def _iter_options__type_error():
    yield 12.6
    yield [12.6]


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_webhooks(input_value):
    """
    Validates whether ``validate_webhooks`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        The value to validate.
    
    Returns
    -------
    output : `None | dict<int, Webhook>`
    
    Raises
    ------
    TypeError
    """
    output = validate_webhooks(input_value)
    vampytest.assert_instance(output, dict, nullable = True)
    return output
