import vampytest

from ..fields import validate_themes
from ..preinstanced import ApplicationTheme


def _iter_options__passing():
    yield (
        None,
        None,
    )
    
    yield (
        [],
        None,
    )
    
    yield (
        [
            ApplicationTheme.business
        ],
        (
            ApplicationTheme.business,
        ),
    )
    
    yield (
        [
            ApplicationTheme.business.value,
        ],
        (
            ApplicationTheme.business,
        ),
    )
    
    yield (
        [
            ApplicationTheme.business,
            ApplicationTheme.action,
        ],
        (
            ApplicationTheme.action,
            ApplicationTheme.business,
        ),
    )


def _iter_options__type_error():
    yield 12.6
    yield [12.6]


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_themes(input_value):
    """
    Tests whether `validate_themes` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Returns
    -------
    output : ``None | tuple<ApplicationTheme>``
    
    Raises
    ------
    TypeError
    """
    output = validate_themes(input_value)
    vampytest.assert_instance(output, tuple, nullable = True)
    
    if (output is not None):
        for element in output:
            vampytest.assert_instance(element, ApplicationTheme)
    
    return output
