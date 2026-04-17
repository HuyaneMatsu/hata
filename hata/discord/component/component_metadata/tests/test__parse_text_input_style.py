import vampytest

from ..constants import TEXT_INPUT_STYLE_DEFAULT
from ..fields import parse_text_input_style
from ..preinstanced import TextInputStyle


def _iter_options():
    yield (
        {},
        TEXT_INPUT_STYLE_DEFAULT,
    )
    
    yield (
        {
            'style': None,
        },
        TextInputStyle.none,
    )
    
    yield (
        {
            'style': TextInputStyle.short.value,
        },
        TextInputStyle.short,
    )
    
    yield (
        {
            'style': TextInputStyle.paragraph.value,
        },
        TextInputStyle.paragraph,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_text_input_style(input_data):
    """
    Tests whether ``parse_text_input_style`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : ``TextInputStyle``
    """
    output = parse_text_input_style(input_data)
    vampytest.assert_instance(output, TextInputStyle)
    return output
