import vampytest

from ..fields import put_font
from ..preinstanced import NameStyleFont


def _iter_options():
    yield (
        NameStyleFont.default,
        False,
        {
            'font_id': NameStyleFont.default.value,
        },
    )
    
    yield (
        NameStyleFont.default,
        True,
        {
            'font_id': NameStyleFont.default.value,
        },
    )
    
    yield (
        NameStyleFont.sakura,
        False,
        {
            'font_id': NameStyleFont.sakura.value,
        },
    )
    
    yield (
        NameStyleFont.sakura,
        True,
        {
            'font_id': NameStyleFont.sakura.value,
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_font(input_value, defaults):
    """
    Tests whether ``put_font`` is working as intended.
    
    Parameters
    ----------
    input_value : ``NameStyleFont``
        Input value.
    
    defaults : `bool`
        Whether fields with their default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    return put_font(input_value, {}, defaults)
