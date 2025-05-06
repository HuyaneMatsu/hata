import vampytest

from ...embed_footer import EmbedFooter

from ..fields import validate_footer


def _iter_options__passing():
    footer = EmbedFooter(text = 'hell')
    
    yield None, None
    yield footer, footer


def _iter_options__type_error():
    yield 12.6


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_footer(input_value):
    """
    Tests whether `validate_footer` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Returns
    -------
    output : ``None | EmbedFooter``
    
    Raises
    ------
    TypeError
    """
    output = validate_footer(input_value)
    vampytest.assert_instance(output, EmbedFooter, nullable = True)
    return output
