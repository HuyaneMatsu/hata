import vampytest

from ....user import User

from ..fields import validate_actioned_by


def test__validate_actioned_by__0():
    """
    Tests whether `validate_actioned_by` works as intended.
    
    Case: passing.
    """
    user = User.precreate(202305160044, name = 'Ken')
    
    for input_value, expected_output in (
        (None, None),
        (user, user),
    ):
        output = validate_actioned_by(input_value)
        vampytest.assert_is(output, expected_output)


def test__validate_actioned_by__1():
    """
    Tests whether `validate_actioned_by` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        'a',
    ):
        with vampytest.assert_raises(TypeError):
            validate_actioned_by(input_value)
