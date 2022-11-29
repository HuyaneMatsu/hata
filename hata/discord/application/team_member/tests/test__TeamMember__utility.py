import vampytest

from ....user import User

from ..preinstanced import TeamMemberPermission, TeamMembershipState
from ..team_member import TeamMember

from .test__TeamMember__constructor import _assert_is_every_attribute_set


def test__TeamMember__copy():
    """
    Tests whether ``TeamMember.copy`` works as intended.
    """
    permissions = [TeamMemberPermission.admin]
    state = TeamMembershipState.invited
    user = User.precreate(202211230010)
    
    team_member = TeamMember(
        permissions = permissions,
        state = state,
        user = user,
    )
    copy = team_member.copy()
    _assert_is_every_attribute_set(copy)
    vampytest.assert_is_not(team_member, copy)
    vampytest.assert_eq(team_member, copy)


def test__TeamMember__copy_with__0():
    """
    Tests whether ``TeamMember.copy_with`` works as intended.
    
    Case: No parameters given.
    """
    permissions = [TeamMemberPermission.admin]
    state = TeamMembershipState.invited
    user = User.precreate(202211230011)
    
    team_member = TeamMember(
        permissions = permissions,
        state = state,
        user = user,
    )
    copy = team_member.copy_with()
    _assert_is_every_attribute_set(copy)
    vampytest.assert_is_not(team_member, copy)
    vampytest.assert_eq(team_member, copy)


def test__TeamMember__copy_with__1():
    """
    Tests whether ``TeamMember.copy_with`` works as intended.
    
    Case: All parameters given.
    """
    old_permissions = [TeamMemberPermission.admin]
    new_permissions = None
    old_state = TeamMembershipState.invited
    new_state = TeamMembershipState.accepted
    old_user = User.precreate(202211230012)
    new_user = User.precreate(202211230013)
    
    team_member = TeamMember(
        permissions = old_permissions,
        state = old_state,
        user = old_user,
    )
    copy = team_member.copy_with(
        permissions = new_permissions,
        state = new_state,
        user = new_user,
    )
    _assert_is_every_attribute_set(copy)
    vampytest.assert_is_not(team_member, copy)
    
    vampytest.assert_is(copy.permissions, None)
    vampytest.assert_is(copy.state, new_state)
    vampytest.assert_is(copy.user, new_user)


def test__TeamMember__iter_permissions():
    """
    Tests whether ``TeamMember.iter_permissions`` works as intended.
    """
    for input_value, expected_output in (
        (None, []),
        ([TeamMemberPermission.admin], [TeamMemberPermission.admin]),
    ):
        team_member = TeamMember(
            permissions = input_value,
        )
        
        vampytest.assert_eq([*team_member.iter_permissions()], expected_output)
