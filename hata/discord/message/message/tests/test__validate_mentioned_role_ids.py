import vampytest

from ....role import Role

from ..fields import validate_mentioned_role_ids


def _iter_options__passing():
    role_id_1 = 202305010017
    role_id_2 = 202305010018
    
    yield None, None
    yield [], None
    yield [role_id_2, role_id_1], (role_id_1, role_id_2)
    yield [Role.precreate(role_id_1)], (role_id_1, )
    
    
def _iter_options__type_error():
    yield 12.6
    yield [12.6]


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_mentioned_role_ids(input_value):
    """
    Tests whether `validate_mentioned_role_ids` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to parse.
    
    Returns
    -------
    output : `None | tuple<int>`
    
    Raises
    ------
    TypeError
    """
    output = validate_mentioned_role_ids(input_value)
    vampytest.assert_instance(output, tuple, nullable = True)
    
    if (output is not None):
        for element in output:
            vampytest.assert_instance(element, int)
    
    return output
        
