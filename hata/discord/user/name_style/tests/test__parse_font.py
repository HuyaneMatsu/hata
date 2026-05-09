import vampytest

from ..fields import parse_font
from ..preinstanced import NameStyleFont


def _iter_options():
    yield (
        {},
        NameStyleFont.default,
    )
    
    yield (
        {
            'font_id': None,
        },
        NameStyleFont.default,
    )
    
    yield (
        {
            'font_id': NameStyleFont.sakura.value
        },
        NameStyleFont.sakura,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_font(input_data):
    """
    Tests whether ``parse_font`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Input data.
    
    Returns
    -------
    output : ``NameStyleFont``
    """
    output = parse_font(input_data)
    vampytest.assert_instance(output, NameStyleFont)
    return output
