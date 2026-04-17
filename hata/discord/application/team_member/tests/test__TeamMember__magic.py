import vampytest

from ....user import User

from ..preinstanced import TeamMemberRole, TeamMembershipState
from ..team_member import TeamMember


def test__TeamMember__repr():
    """
    Tests whether ``TeamMember.__repr__`` works as intended.
    """
    role = TeamMemberRole.admin
    state = TeamMembershipState.invited
    user = User.precreate(202211230006)
    
    team_member = TeamMember(
        role = role,
        state = state,
        user = user,
    )
    
    vampytest.assert_instance(repr(team_member), str)


def test__TeamMember__hash():
    """
    Tests whether ``TeamMember.__hash__`` works as intended.
    """
    role = TeamMemberRole.admin
    state = TeamMembershipState.invited
    user = User.precreate(202211230007)
    
    team_member = TeamMember(
        role = role,
        state = state,
        user = user,
    )
    
    vampytest.assert_instance(hash(team_member), int)


def test__TeamMember__eq():
    """
    Tests whether ``TeamMember.__eq__`` works as intended.
    """
    role = TeamMemberRole.admin
    state = TeamMembershipState.invited
    user = User.precreate(202211230008)
    
    keyword_parameters = {
        'role': role,
        'state': state,
        'user': user,
    }
    
    team_member = TeamMember(**keyword_parameters)
    vampytest.assert_eq(team_member, team_member)
    vampytest.assert_ne(team_member, object())
    
    for field_name, field_value in (
        ('role', TeamMemberRole.owner),
        ('state', TeamMembershipState.accepted),
        ('user', User.precreate(202211230009)),
    ):
        test_team_member = TeamMember(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(team_member, test_team_member)


def tst__TeamMember__sort():
    """
    Tests whether sorting team members is working as intended.
    """
    team_member_0 = TeamMember(user = User.precreate(202211240039))
    team_member_1 = TeamMember(user = User.precreate(202211240040))
    
    vampytest.assert_eq(sorted([team_member_1, team_member_0]), [team_member_0, team_member_1])
