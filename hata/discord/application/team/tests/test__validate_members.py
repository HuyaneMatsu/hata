import vampytest

from ....user import User

from ...team_member import TeamMember

from ..fields import validate_members


def test__validate_members__0():
    """
    Tests whether ``validate_members`` works as intended.
    
    Case: passing.
    """
    team_member = TeamMember(user = User.precreate(202211230022))
    
    for input_parameter, expected_output in (
        (None, None),
        ([], None),
        ([team_member], (team_member, ))
    ):
        output = validate_members(input_parameter)
        vampytest.assert_eq(output, expected_output)


def test__validate_members__1():
    """
    Tests whether ``validate_members`` works as intended.
    
    Case: `TypeError`.
    """
    for input_parameter in (
        12.6,
        [12.6],
    ):
        with vampytest.assert_raises(TypeError):
            validate_members(input_parameter)
