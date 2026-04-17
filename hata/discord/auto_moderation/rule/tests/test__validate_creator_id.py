import vampytest

from ....user import User

from ..fields import validate_creator_id


def test__validate_creator_id__0():
    """
    Tests whether ``validate_creator_id`` works as intended.
    
    Case: passing.
    """
    creator_id = 202211170030
    
    for input_value, expected_output in (
        (None, 0),
        (creator_id, creator_id),
        (User.precreate(creator_id), creator_id),
        (str(creator_id), creator_id)
    ):
        output = validate_creator_id(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_creator_id__1():
    """
    Tests whether ``validate_creator_id`` works as intended.
    
    Case: `ValueError`.
    """
    for input_value in (
        '-1',
        -1,
    ):
        with vampytest.assert_raises(AssertionError, ValueError):
            validate_creator_id(input_value)


def test__validate_creator_id__2():
    """
    Tests whether ``validate_creator_id`` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_creator_id(input_value)
