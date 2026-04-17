import vampytest

from ....user import User, ZEROUSER

from ...team import Team

from ..fields import validate_owner


def test__validate_owner__0():
    """
    Tests whether ``validate_owner`` works as intended.
    
    Case: Passing.
    """
    user = User.precreate(202211270021)
    team = Team.precreate(202211270022)
    
    for input_value, expected_output in (
        (None, ZEROUSER),
        (user, user),
        (team, team),
    ):
        owner = validate_owner(input_value)
        vampytest.assert_is(owner, expected_output)


def test__validate_owner__1():
    """
    Tests whether ``validate_owner`` works as intended.
    
    Case: `TypeError`
    """
    for field_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_owner(field_value)
