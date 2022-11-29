import vampytest

from ....user import ClientUserBase, User

from ..preinstanced import TeamMemberPermission, TeamMembershipState
from ..team_member import TeamMember


def _assert_is_every_attribute_set(team_member):
    """
    Asserts whether all attributes of the given team member are set.
    
    Parameters
    ----------
    team_member : ``TeamMember``
        The team member to check.
    """
    vampytest.assert_instance(team_member, TeamMember)
    vampytest.assert_instance(team_member.permissions, tuple, nullable = True)
    vampytest.assert_instance(team_member.state, TeamMembershipState)
    vampytest.assert_instance(team_member.user, ClientUserBase)


def test__TeamMember__new__0():
    """
    Tests whether ``TeamMember.__new__`` works as intended.
    
    Case: No parameters given.
    """
    team_member = TeamMember()
    _assert_is_every_attribute_set(team_member)


def test__TeamMember__new__1():
    """
    Tests whether ``TeamMember.__new__`` works as intended.
    
    Case: All parameters given.
    """
    permissions = [TeamMemberPermission.admin]
    state = TeamMembershipState.invited
    user = User.precreate(202211230003)
    
    team_member = TeamMember(
        permissions = permissions,
        state = state,
        user = user,
        
    )
    _assert_is_every_attribute_set(team_member)
    
    vampytest.assert_eq(team_member.permissions, tuple(permissions))
    vampytest.assert_is(team_member.state, state)
    vampytest.assert_is(team_member.user, user)
