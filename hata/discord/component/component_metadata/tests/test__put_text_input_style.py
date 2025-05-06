import vampytest

from ..fields import put_text_input_style
from ..preinstanced import TextInputStyle


def _iter_options():
    yield TextInputStyle.short, False, {'style': TextInputStyle.short.value}
    yield TextInputStyle.short, True, {'style': TextInputStyle.short.value}
    yield TextInputStyle.paragraph, False, {'style': TextInputStyle.paragraph.value}
    yield TextInputStyle.paragraph, True, {'style': TextInputStyle.paragraph.value}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_text_input_style(input_value, defaults):
    """
    Tests whether ``put_text_input_style`` is working as intended.
    
    Parameters
    ----------
    input_value : ``SeparatorSpacingSize``
        The value to serialise.
    
    defaults : `bool`
        Whether values with their default value should be included in the output as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_text_input_style(input_value, {}, defaults)
