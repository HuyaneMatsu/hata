import vampytest

from ....bases import Icon, IconType
from ....user import User

from ...team_member import TeamMember

from ..team import Team

from .test__Team__constructor import _assert_is_every_attribute_set


def test__Team__from_data__0():
    """
    Tests whether ``Team.from_data`` works as intended.
    
    Case: Default.
    """
    team_id = 202211240008
    icon = Icon(IconType.static, 2)
    members = [TeamMember(user = User.precreate(202211240009))]
    name = 'Red'
    owner_id = 202211240010
    
    data = {
        'id': str(team_id),
        'icon': icon.as_base_16_hash,
        'members': [member.to_data(defaults = True, include_internals = True) for member in members],
        'name': name,
        'owner_user_id': str(owner_id)
    }
    
    team = Team.from_data(data)
    _assert_is_every_attribute_set(team)
    vampytest.assert_eq(team.id, team_id)
    
    vampytest.assert_eq(team.icon, icon)
    vampytest.assert_eq(team.members, tuple(members))
    vampytest.assert_eq(team.name, name)
    vampytest.assert_eq(team.owner_id, owner_id)



def test__Team__from_data__1():
    """
    Tests whether ``Team.from_data`` works as intended.
    
    Case: Check caching.
    """
    team_id = 202211240011
    
    data = {
        'id': str(team_id),
    }
    
    team = Team.from_data(data)
    test_team = Team.from_data(data)
    
    vampytest.assert_eq(team, test_team)


def test__Team__to_data():
    """
    Tests whether ``Team.to_data`` works as intended.
    
    Case: include defaults and internals.
    """
    team_id = 202211240012
    icon = Icon(IconType.static, 2)
    members = [TeamMember(user = User.precreate(202211240013))]
    name = 'Red'
    owner_id = 202211240014
    
    expected_output = {
        'id': str(team_id),
        'icon': icon.as_base_16_hash,
        'members': [member.to_data(defaults = True, include_internals = True) for member in members],
        'name': name,
        'owner_user_id': str(owner_id)
    }
    
    team = Team.precreate(
        team_id,
        icon = icon,
        members = members,
        name = name,
        owner_id = owner_id,
    )
    
    vampytest.assert_eq(team.to_data(defaults = True, include_internals = True), expected_output)


def test__Team__to_data_user():
    """
    Tests whether ``Team.to_data_user`` works as intended.
    """
    team_id = 202211270018
    icon = Icon(IconType.static, 2)
    members = [TeamMember(user = User.precreate(202211270019))]
    name = 'Red'
    owner_id = 202211270020
    
    team = Team.precreate(
        team_id,
        icon = icon,
        members = members,
        name = name,
        owner_id = owner_id,
    )
    
    data = team.to_data_user()
    vampytest.assert_instance(data, dict)
    vampytest.assert_in('id', data)
    vampytest.assert_eq(data['id'], str(team_id))
