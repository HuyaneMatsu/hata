import vampytest

from ....color import Color

from ...role_color_configuration import RoleColorConfiguration

from ..fields import validate_color_configuration


def _iter_options__passing():
    color_primary = Color(123)
    color_secondary = Color(234)
    color_tertiary = Color(345)
    
    role_color_configuration = RoleColorConfiguration(
        color_primary = color_primary,
        color_secondary = color_secondary,
        color_tertiary = color_tertiary,
    )
    
    yield None, RoleColorConfiguration.create_empty()
    yield role_color_configuration, role_color_configuration


def _iter_options__type_error():
    yield 12.6


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_color_configuration(input_value):
    """
    Tests whether `validate_color_configuration` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        The value to validate.
    
    Returns
    -------
    output : ``RoleColorConfiguration``
    
    Raises
    ------
    TypeError
    """
    output = validate_color_configuration(input_value)
    vampytest.assert_instance(output, RoleColorConfiguration)
    return output
