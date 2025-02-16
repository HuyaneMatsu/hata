import vampytest

from ....user import User

from ...team_member import TeamMember

from ..fields import put_members


def test__put_members():
    """
    Tests whether ``put_members`` works as intended.
    
    Case: include internals.
    """
    team_member = TeamMember(user = User.precreate(202211230021))
    
    for input_value, defaults, expected_output in (
        (None, True, {'members': []}),
        ([team_member], False, {'members': [team_member.to_data(defaults = False, include_internals = True)]}),
    ):
        data = put_members(input_value, {}, defaults, include_internals = True)
        vampytest.assert_eq(data, expected_output)
