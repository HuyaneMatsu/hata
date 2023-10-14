import vampytest

from ...entity_select_default_value import EntitySelectDefaultValue, EntitySelectDefaultValueType

from ..fields import validate_default_values


def _iter_options():
    option_0 = EntitySelectDefaultValue(EntitySelectDefaultValueType.user, 202310130004)
    option_1 = EntitySelectDefaultValue(EntitySelectDefaultValueType.role, 202310130005)
    
    yield None, None
    yield [], None
    yield [option_0], (option_0,)
    yield [option_0, option_1], (option_0, option_1,)


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__validate_default_values__passing(input_value):
    """
    Tests whether ``validate_default_values`` works as intended.
    
    Case: passing.
    
    Parameters
    ----------
    input_value : `object`
        The value to validate.
    
    Returns
    -------
    output : `None | tuple<EntitySelectDefaultValue>`
    """
    return validate_default_values(input_value)


@vampytest.raising(TypeError)
@vampytest.call_with(12.6)
@vampytest.call_with([13.6])
def test__validate_default_values__type_error(input_value):
    """
    Tests whether ``validate_default_values`` works as intended.
    
    Case: `TypeError`.
    
    Parameters
    ----------
    input_value : `object`
        The value to validate.
    
    Raises
    ------
    TypeError
    """
    validate_default_values(input_value)
