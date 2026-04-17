import vampytest

from ....user import User

from ..preinstanced import TeamMemberRole, TeamMembershipState
from ..team_member import TeamMember

from .test__TeamMember__constructor import _assert_fields_set


def test__TeamMember__copy():
    """
    Tests whether ``TeamMember.copy`` works as intended.
    """
    role = TeamMemberRole.admin
    state = TeamMembershipState.invited
    user = User.precreate(202211230010)
    
    team_member = TeamMember(
        role = role,
        state = state,
        user = user,
    )
    copy = team_member.copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(team_member, copy)
    vampytest.assert_eq(team_member, copy)


def test__TeamMember__copy_with__0():
    """
    Tests whether ``TeamMember.copy_with`` works as intended.
    
    Case: No parameters given.
    """
    role = TeamMemberRole.admin
    state = TeamMembershipState.invited
    user = User.precreate(202211230011)
    
    team_member = TeamMember(
        role = role,
        state = state,
        user = user,
    )
    copy = team_member.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_is_not(team_member, copy)
    vampytest.assert_eq(team_member, copy)


def test__TeamMember__copy_with__1():
    """
    Tests whether ``TeamMember.copy_with`` works as intended.
    
    Case: All parameters given.
    """
    old_role = TeamMemberRole.admin
    new_role = TeamMemberRole.owner
    old_state = TeamMembershipState.invited
    new_state = TeamMembershipState.accepted
    old_user = User.precreate(202211230012)
    new_user = User.precreate(202211230013)
    
    team_member = TeamMember(
        role = old_role,
        state = old_state,
        user = old_user,
    )
    copy = team_member.copy_with(
        role = new_role,
        state = new_state,
        user = new_user,
    )
    _assert_fields_set(copy)
    vampytest.assert_is_not(team_member, copy)
    
    vampytest.assert_is(copy.role, TeamMemberRole.owner)
    vampytest.assert_is(copy.state, new_state)
    vampytest.assert_is(copy.user, new_user)
