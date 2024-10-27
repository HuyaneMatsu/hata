import vampytest

from ..helpers import _validate_name


def _iter_options__passing():
    yield 'elly', 'elly'
    yield '', None
    yield None, None


def _iter_options__type_error():
    yield object()


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_name(input_value):
    """
    Tests whether ``_validate_name`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        The validate.
    
    Returns
    -------
    output : `None | str`
    
    Raises
    ------
    TypeError
    """
    output = _validate_name(input_value)
    vampytest.assert_instance(output, str, nullable = True)
    return output
