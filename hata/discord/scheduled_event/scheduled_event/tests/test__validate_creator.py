import vampytest

from ....user import User

from ..fields import validate_creator


def test__validate_creator__0():
    """
    Tests whether `validate_creator` works as intended.
    
    Case: passing.
    """
    creator = User.precreate(202303140005, name = 'Orin')
    
    for input_value, expected_output in (
        (creator, creator),
    ):
        output = validate_creator(input_value)
        vampytest.assert_is(output, expected_output)


def test__validate_creator__1():
    """
    Tests whether `validate_creator` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        'a',
    ):
        with vampytest.assert_raises(TypeError):
            validate_creator(input_value)
