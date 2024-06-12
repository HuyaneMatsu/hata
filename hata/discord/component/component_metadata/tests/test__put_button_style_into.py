import vampytest

from ..constants import BUTTON_STYLE_DEFAULT
from ..fields import put_button_style_into
from ..preinstanced import ButtonStyle


def _iter_options():
    yield BUTTON_STYLE_DEFAULT, False, {'style': BUTTON_STYLE_DEFAULT.value}
    yield BUTTON_STYLE_DEFAULT, True, {'style': BUTTON_STYLE_DEFAULT.value}
    yield ButtonStyle.link, False, {'style': ButtonStyle.link.value}
    yield ButtonStyle.link, True, {'style': ButtonStyle.link.value}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_button_style_into(input_value, defaults):
    """
    Tests whether ``put_button_style_into`` is working as intended.
    
    Parameters
    ----------
    input_value : ``ButtonStyle``
        The value to serialise.
    defaults : `bool`
        Whether values with their default value should be included in the output as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_button_style_into(input_value, {}, defaults)
