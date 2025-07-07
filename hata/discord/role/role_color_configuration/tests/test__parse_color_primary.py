import vampytest

from ....color import Color

from ..fields import parse_color_primary


def _iter_options():
    yield (
        {},
        Color(0),
    )
    
    yield (
        {
            'primary_color': None,
        },
        Color(0),
    )
    
    yield (
        {
            'primary_color': 1,
        },
        Color(1),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_color_primary(input_data):
    """
    Tests whether ``parse_color_primary`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : ``Color``
    """
    output = parse_color_primary(input_data)
    vampytest.assert_instance(output, Color)
    return output
