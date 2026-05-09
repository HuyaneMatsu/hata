import vampytest

from ...name_style import NameStyle, NameStyleFont

from ..fields import parse_name_style


def _iter_options():
    name_style = NameStyle(font = NameStyleFont.tempo)
    
    yield (
        {},
        None,
    )
    
    yield (
        {
            'display_name_styles': None,
        },
        None,
    )
    
    yield (
        {
            'display_name_styles': name_style.to_data(),
        },
        name_style,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_name_style(input_data):
    """
    Tests whether ``parse_name_style`` works as intended.
    
    Parameters
    ----------
    input_data : dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : ``None | NameStyle``
    """
    output = parse_name_style(input_data)
    vampytest.assert_instance(output, NameStyle, nullable = True)
    return output
