import vampytest

from ...activity_secrets import ActivitySecrets

from ..fields import validate_secrets


def _iter_options__passing():
    secrets = ActivitySecrets(join = 'hell')
    
    yield None, None
    yield secrets, secrets


def _iter_options__type_error():
    yield 12.6


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_secrets(input_value):
    """
    Tests whether `validate_secrets` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Returns
    -------
    output : `None | ActivitySecrets`
    
    Raises
    ------
    TypeError
    """
    output = validate_secrets(input_value)
    vampytest.assert_instance(output, ActivitySecrets, nullable = True)
    return output
