import vampytest

from ....color import Color

from ..fields import parse_colors


def _iter_options():
    color_0 = Color(1233)
    color_1 = Color(1236)
    
    yield (
        {},
        None,
    )
    
    yield (
        {
            'colors': [
                format(color_0, 'X'),
                format(color_1, 'X')
            ],
        },
        (
            color_0,
            color_1,
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_colors(input_data):
    """
    Tests whether ``parse_colors`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Input data.
    
    Returns
    -------
    output : ``None | tuple<Color>``
    """
    output = parse_colors(input_data)
    
    vampytest.assert_instance(output, tuple, nullable = True)
    if (output is not None):
        for element in output:
            vampytest.assert_instance(element, Color)

    return output
