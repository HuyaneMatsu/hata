import vampytest

from ....color import Color

from ...role_color_configuration import RoleColorConfiguration

from ..fields import parse_color_configuration


def _iter_options():
    color_primary = Color(123)
    color_secondary = Color(234)
    color_tertiary = Color(345)
    
    role_color_configuration = RoleColorConfiguration(
        color_primary = color_primary,
        color_secondary = color_secondary,
        color_tertiary = color_tertiary,
    )
    
    yield (
        {},
        RoleColorConfiguration.create_empty(),
    )
    
    yield (
        {
            'colors': None,
        },
        RoleColorConfiguration.create_empty(),
    )
    
    yield (
        {
            'colors': role_color_configuration.to_data(),
        },
        role_color_configuration,
    )
    
    yield (
        {
            'color': int(color_primary),
        },
        role_color_configuration.create_from_color_primary(color_primary),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_color_configuration(input_data):
    """
    Tests whether ``parse_color_configuration`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : ``RoleColorConfiguration``
    """
    output = parse_color_configuration(input_data)
    vampytest.assert_instance(output, RoleColorConfiguration)
    return output
