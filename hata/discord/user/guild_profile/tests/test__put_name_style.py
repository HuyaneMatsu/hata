import vampytest

from ...name_style import NameStyle, NameStyleFont

from ..fields import put_name_style


def _iter_options():
    name_style = NameStyle(font = NameStyleFont.tempo)
    
    yield (
        None,
        False,
        {},
    )
    
    yield (
        None,
        True,
        {
            'display_name_styles': None,
        },
    )
    
    yield (
        name_style,
        False,
        {
            'display_name_styles': name_style.to_data(defaults = False),
        },
    )
    
    yield (
        name_style,
        True,
        {
            'display_name_styles': name_style.to_data(defaults = True),
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_name_style(input_value, defaults):
    """
    Tests whether ``put_name_style`` is working as intended.
    
    Parameters
    ----------
    input_value : ``None | NameStyle``
        Value to serialise.
    
    defaults : `bool`
        Whether fields with their default value should be included.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_name_style(input_value, {}, defaults)
