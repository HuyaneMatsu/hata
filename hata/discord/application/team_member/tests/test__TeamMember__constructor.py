import vampytest

from ....user import ClientUserBase, User

from ..preinstanced import TeamMemberRole, TeamMembershipState
from ..team_member import TeamMember


def _assert_fields_set(team_member):
    """
    Asserts whether all attributes of the given team member are set.
    
    Parameters
    ----------
    team_member : ``TeamMember``
        The team member to check.
    """
    vampytest.assert_instance(team_member, TeamMember)
    vampytest.assert_instance(team_member.role, TeamMemberRole)
    vampytest.assert_instance(team_member.state, TeamMembershipState)
    vampytest.assert_instance(team_member.user, ClientUserBase)


def test__TeamMember__new__no_fields():
    """
    Tests whether ``TeamMember.__new__`` works as intended.
    
    Case: No parameters given.
    """
    team_member = TeamMember()
    _assert_fields_set(team_member)


def test__TeamMember__new__all_fields():
    """
    Tests whether ``TeamMember.__new__`` works as intended.
    
    Case: All parameters given.
    """
    role = TeamMemberRole.admin
    state = TeamMembershipState.invited
    user = User.precreate(202211230003)
    
    team_member = TeamMember(
        role = role,
        state = state,
        user = user,
        
    )
    _assert_fields_set(team_member)
    
    vampytest.assert_is(team_member.role, role)
    vampytest.assert_is(team_member.state, state)
    vampytest.assert_is(team_member.user, user)
