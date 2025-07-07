import vampytest

from ....color import Color

from ...role_color_configuration import RoleColorConfiguration

from ..fields import put_color_configuration


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
        role_color_configuration,
        False,
        {
            'colors': role_color_configuration.to_data(defaults = False),
        },
    )
    
    yield (
        role_color_configuration,
        True,
        {
            'colors': role_color_configuration.to_data(defaults = True),
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_color_configuration(input_value, defaults):
    """
    Tests whether ``put_color_configuration`` is working as intended.
    
    Parameters
    ----------
    value : ``RoleColorConfiguration``
        Value to serialize.
    
    defaults : `bool`
        Whether to include values as their default.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_color_configuration(input_value, {}, defaults)
