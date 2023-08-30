import vampytest

from ....user import User

from ..preinstanced import TeamMemberRole, TeamMembershipState
from ..team_member import TeamMember

from .test__TeamMember__constructor import _assert_fields_set


def test__TeamMember__from_data():
    """
    Tests whether ``TeamMember.from_data`` works as intended.
    """
    role = TeamMemberRole.admin
    state = TeamMembershipState.invited
    user = User.precreate(202211230004)
    
    data = {
        'role': role.value,
        'membership_state': state.value,
        'user': user.to_data(defaults = True, include_internals = True),
    }
    
    team_member = TeamMember.from_data(data)
    _assert_fields_set(team_member)
    
    vampytest.assert_is(team_member.role, role)
    vampytest.assert_is(team_member.state, state)
    vampytest.assert_is(team_member.user, user)


def test__TeamMember__to_data():
    """
    Tests whether ``TeamMember.to_data`` works as intended.
    
    Case: Include defaults & internals.
    """
    role = TeamMemberRole.admin
    state = TeamMembershipState.invited
    user = User.precreate(202211230005)
    
    team_member = TeamMember(
        role = role,
        state = state,
        user = user,
    )
    
    expected_output = {
        'role': role.value,
        'membership_state': state.value,
        'user': user.to_data(defaults = True, include_internals = True),
    }
    
    vampytest.assert_eq(team_member.to_data(defaults = True, include_internals = True), expected_output)
