import vampytest

from ....user import User

from ...team_member import TeamMember

from ..fields import parse_members


def test__parse_members():
    """
    Tests whether ``parse_members`` works as intended.
    """
    team_member = TeamMember(user = User.precreate(202211230020))
    
    for input_data, expected_output in (
        ({}, None),
        ({'members': None}, None),
        ({'members': []}, None),
        ({'members': [team_member.to_data(defaults = True)]}, (team_member, ))
    ):
        output = parse_members(input_data)
        
        vampytest.assert_eq(output, expected_output)
