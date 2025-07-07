import vampytest

from ....color import Color

from ..role_color_configuration import RoleColorConfiguration


def test__RoleColorConfiguration__repr():
    """
    Tests whether ``RoleColorConfiguration.__repr__`` works as intended.
    """
    color_primary = Color(123)
    color_secondary = Color(234)
    color_tertiary = Color(345)
    
    role_color_configuration = RoleColorConfiguration(
        color_primary = color_primary,
        color_secondary = color_secondary,
        color_tertiary = color_tertiary,
    )
    
    output = repr(role_color_configuration)
    vampytest.assert_instance(output, str)


def test__RoleColorConfiguration__hash():
    """
    Tests whether ``RoleColorConfiguration.__hash__`` works as intended.
    """
    color_primary = Color(123)
    color_secondary = Color(234)
    color_tertiary = Color(345)
    
    role_color_configuration = RoleColorConfiguration(
        color_primary = color_primary,
        color_secondary = color_secondary,
        color_tertiary = color_tertiary,
    )
    
    output = hash(role_color_configuration)
    vampytest.assert_instance(output, int)


def _iter_options__eq():
    color_primary = Color(123)
    color_secondary = Color(234)
    color_tertiary = Color(345)
    
    keyword_parameters = {
        'color_primary': color_primary,
        'color_secondary': color_secondary,
        'color_tertiary': color_tertiary,
    }
    
    yield (
        keyword_parameters,
        keyword_parameters,
        True,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'color_primary': Color(666),
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'color_secondary': Color(777),
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'color_tertiary': Color(888),
        },
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__RoleColorConfiguration__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``RoleColorConfiguration.__eq__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters_0 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    keyword_parameters_1 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : `bool`
    """
    role_color_configuration_0 = RoleColorConfiguration(**keyword_parameters_0)
    role_color_configuration_1 = RoleColorConfiguration(**keyword_parameters_1)
    
    output = role_color_configuration_0 == role_color_configuration_1
    vampytest.assert_instance(output, bool)
    return output
