import vampytest

from ....bases import Icon, IconType
from ....user import ClientUserBase, User

from ...team_member import TeamMember, TeamMembershipState

from ..team import Team

from .test__Team__constructor import _assert_is_every_attribute_set


def test__Team__copy():
    """
    Tests whether ``Team.copy`` works as intended.
    """
    icon = Icon(IconType.static, 2)
    members = [TeamMember(user = User.precreate(202211240025))]
    name = 'Red'
    owner_id = 202211240026
    
    
    team = Team(
        icon = icon,
        members = members,
        name = name,
        owner_id = owner_id,
    )
    
    copy = team.copy()
    _assert_is_every_attribute_set(copy)
    vampytest.assert_eq(copy, team)
    vampytest.assert_not_is(copy, team)


def test__Team__copy_with__0():
    """
    Tests whether ``Team.copy_with`` works as intended.
    
    Case: No parameters given.
    """
    icon = Icon(IconType.static, 2)
    members = [TeamMember(user = User.precreate(202211240026))]
    name = 'Red'
    owner_id = 202211240027
    
    
    team = Team(
        icon = icon,
        members = members,
        name = name,
        owner_id = owner_id,
    )
    
    copy = team.copy_with()
    _assert_is_every_attribute_set(copy)
    vampytest.assert_eq(copy, team)
    vampytest.assert_not_is(copy, team)


def test__Team__copy_with__1():
    """
    Tests whether ``Team.copy_with`` works as intended.
    
    Case: Stuffed.
    """
    old_icon = Icon(IconType.static, 2)
    new_icon = Icon(IconType.animated, 12)
    old_members = [TeamMember(user = User.precreate(202211240026))]
    new_members = [TeamMember(user = User.precreate(202211240027)), TeamMember(user = User.precreate(202211240028))]
    old_name = 'Red'
    new_name = 'Angel'
    old_owner_id = 202211240029
    new_owner_id = 202211240030
    
    
    team = Team(
        icon = old_icon,
        members = old_members,
        name = old_name,
        owner_id = old_owner_id,
    )
    
    copy = team.copy_with(
        icon = new_icon,
        members = new_members,
        name = new_name,
        owner_id = new_owner_id,
    )
    _assert_is_every_attribute_set(copy)
    vampytest.assert_not_is(copy, team)

    vampytest.assert_eq(copy.icon, new_icon)
    vampytest.assert_eq(copy.members, tuple(new_members))
    vampytest.assert_eq(copy.name, new_name)
    vampytest.assert_eq(copy.owner_id, new_owner_id)


def test__Team__owner():
    """
    Tests whether ``Team.owner`` works as intended.
    """
    owner_id = 202211240031
    
    team = Team(owner_id = owner_id)
    
    owner = team.owner
    vampytest.assert_instance(owner, ClientUserBase)
    vampytest.assert_eq(owner.id, owner_id)


def test__Team__iter_members():
    """
    Tests whether ``Team.iter_members`` works as intended.
    """
    member_0 = TeamMember(user = User.precreate(202211240032))
    member_1 = TeamMember(user = User.precreate(202211240033))
    
    for input_value, expected_output in (
        (None, []),
        ([member_0], [member_0]),
        ([member_0, member_1], [member_0, member_1]),
    ):
        team = Team(members = input_value)
        vampytest.assert_eq([*team.iter_members()], expected_output)


def test__Team__invited():
    """
    Tests whether ``Team.invited`` works as intended.
    """
    user_0 = User.precreate(202211240034)
    user_1 = User.precreate(202211240035)
    member_0 = TeamMember(user = user_0, state = TeamMembershipState.invited)
    member_1 = TeamMember(user = user_1, state = TeamMembershipState.accepted)
    
    team = Team(members = [member_0, member_1])
    vampytest.assert_eq(team.invited, [user_0])


def test__Team__accepted():
    """
    Tests whether ``Team.accepted`` works as intended.
    """
    user_0 = User.precreate(202211240036)
    user_1 = User.precreate(202211240037)
    member_0 = TeamMember(user = user_0, state = TeamMembershipState.invited)
    member_1 = TeamMember(user = user_1, state = TeamMembershipState.accepted)
    
    team = Team(members = [member_0, member_1])
    vampytest.assert_eq(team.accepted, [user_1])


def test__Team__partial():
    """
    Tests whether ``Team.accepted`` works as intended.
    """
    team_id = 202211240038
    
    team = Team()
    vampytest.assert_true(team.partial)
    
    
    team = Team.precreate(team_id)
    vampytest.assert_false(team.partial)
