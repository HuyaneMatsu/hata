import vampytest

from ..fields import validate_id


def _iter_options__passing():
    integration_account_id = 'koishi'
    
    yield None, ''
    yield '', ''
    yield integration_account_id, integration_account_id


def _iter_options__type_error():
    yield 12.6


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_id(input_value):
    """
    Tests whether `validate_id` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Input value to validate.
    
    Returns
    -------
    output : `str`
    
    Raises
    ------
    TypeError
    """
    output = validate_id(input_value)
    vampytest.assert_instance(output, str)
    return output
