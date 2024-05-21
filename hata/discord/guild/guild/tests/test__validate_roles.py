import vampytest

from ....role import Role

from ..fields import validate_roles


def _iter_options__passing():
    role_id = 202306080008
    role_name = 'Koishi'
    
    role = Role.precreate(
        role_id,
        name = role_name,
    )
    
    yield None, {}
    yield [], {}
    yield {}, {}
    yield [role], {role_id: role}
    yield {role_id: role}, {role_id: role}

    
@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
def test__validate_roles__passing(input_value):
    """
    Tests whether ``validate_roles`` works as intended.
    
    Case: passing.
    
    Parameters
    ----------
    input_value : `object`
        Value to pass to the validators.
    
    Returns
    -------
    expected_output : `None | dict<int, Role>`
    """
    return validate_roles(input_value)


def _iter_options__type_error():
    yield 12.6
    yield [12.6]
    yield {12.6: 12.6}


@vampytest.raising(TypeError)
@vampytest.call_from(_iter_options__type_error())
def test__validate_roles__type_error(input_value):
    """
    Tests whether ``validate_roles`` works as intended.
    
    Case: `TypeError`.
    
    Parameters
    ----------
    input_value : `object`
        Value to pass to the validators.
    
    Raises
    ------
    TypeError
        The occurred exception.
    """
    validate_roles(input_value)
