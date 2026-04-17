import vampytest

from ....bases import Icon, IconType
from ....user import User

from ...team_member import TeamMember

from ..team import Team


def test__Team__repr():
    """
    Tests whether ``Team.__repr__`` works as intended.
    
    Case: include defaults and internals.
    """
    team_id = 202211240015
    icon = Icon(IconType.static, 2)
    members = [TeamMember(user = User.precreate(202211240016))]
    name = 'Red'
    owner_id = 202211240017
    
    
    team = Team.precreate(
        team_id,
        icon = icon,
        members = members,
        name = name,
        owner_id = owner_id,
    )
    
    vampytest.assert_instance(repr(team), str)


def test__Team__hash():
    """
    Tests whether ``Team.__hash__`` works as intended.
    
    Case: include defaults and internals.
    """
    team_id = 202211240018
    icon = Icon(IconType.static, 2)
    members = [TeamMember(user = User.precreate(202211240019))]
    name = 'Red'
    owner_id = 202211240020
    
    team = Team.precreate(
        team_id,
        icon = icon,
        members = members,
        name = name,
        owner_id = owner_id,
    )
    
    vampytest.assert_instance(hash(team), int)


def test__Team__eq():
    """
    Tests whether ``Team.__eq__`` works as intended.
    
    Case: include defaults and internals.
    """
    team_id = 202211240021
    icon = Icon(IconType.static, 2)
    members = [TeamMember(user = User.precreate(202211240022))]
    name = 'Red'
    owner_id = 202211240023
    
    keyword_parameters = {
        'icon': icon,
        'members': members,
        'name': name,
        'owner_id': owner_id,
    }
    
    team = Team.precreate(team_id, **keyword_parameters)
    
    vampytest.assert_eq(team, team)
    vampytest.assert_ne(team, object())
    
    test_team = Team(**keyword_parameters)
    vampytest.assert_eq(team, test_team)
    
    for field_name, field_value in (
        ('icon', None),
        ('members', None),
        ('name', 'Suwako'),
        ('owner_id', 202211240024),
    ):
        test_team = Team(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(team, test_team)
