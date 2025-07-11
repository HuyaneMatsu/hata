import vampytest

from ....color import Color

from ..fields import parse_color_secondary


def _iter_options():
    yield (
        {},
        None,
    )
    
    yield (
        {
            'secondary_color': None,
        },
        None,
    )
    
    yield (
        {
            'secondary_color': 1,
        },
        Color(1),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_color_secondary(input_data):
    """
    Tests whether ``parse_color_secondary`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : ``None | Color``
    """
    output = parse_color_secondary(input_data)
    vampytest.assert_instance(output, Color, nullable = True)
    return output
