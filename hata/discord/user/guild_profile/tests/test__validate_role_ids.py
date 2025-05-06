import vampytest

from ....role import Role

from ..fields import validate_role_ids


def _iter_options__passing():
    role_id_0 = 202210280003
    role_id_1 = 202210280004
    
    yield None, None
    yield [], None
    yield [role_id_0, role_id_1], (role_id_0, role_id_1)
    yield [role_id_1, role_id_0], (role_id_0, role_id_1)
    yield [Role.precreate(role_id_0), Role.precreate(role_id_1)], (role_id_0, role_id_1)


def _iter_options__type_error():
    yield 12.6
    yield [12.6]


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_role_ids(input_value):
    """
    Tests whether `validate_role_ids` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Returns
    -------
    output : `None | tuple<int>`
    
    Raises
    ------
    TypeError
    """
    output = validate_role_ids(input_value)
    vampytest.assert_instance(output, tuple, nullable = True)
    return output
