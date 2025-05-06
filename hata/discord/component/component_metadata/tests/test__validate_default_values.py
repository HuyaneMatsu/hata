import vampytest

from ...entity_select_default_value import EntitySelectDefaultValue, EntitySelectDefaultValueType

from ..fields import validate_default_values


def _iter_options__passing():
    option_0 = EntitySelectDefaultValue(EntitySelectDefaultValueType.user, 202310130004)
    option_1 = EntitySelectDefaultValue(EntitySelectDefaultValueType.role, 202310130005)
    
    yield None, None
    yield [], None
    yield [option_0], (option_0,)
    yield [option_0, option_1], (option_0, option_1,)


def _iter_options__type_error():
    yield 12.6
    yield [12.6]


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_default_values(input_value):
    """
    Tests whether ``validate_default_values`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        The value to validate.
    
    Returns
    -------
    output : ``None | tuple<EntitySelectDefaultValue>``
    Raises
    ------
    TypeError
    """
    output =  validate_default_values(input_value)
    vampytest.assert_instance(output, tuple, nullable = True)
    return output
