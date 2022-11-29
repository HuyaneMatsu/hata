import vampytest

from ....bases import Icon, IconType
from ....user import User

from ...team_member import TeamMember

from ..team import Team


def _assert_is_every_attribute_set(team):
    """
    Asserts whether every attributes of the given are set.
    
    Parameters
    ----------
    team : ``Team``
        The team to check.
    """
    vampytest.assert_instance(team, Team)
    vampytest.assert_instance(team.icon_hash, int)
    vampytest.assert_instance(team.icon_type, IconType)
    vampytest.assert_instance(team.id, int)
    vampytest.assert_instance(team.members, tuple, nullable = True)
    vampytest.assert_instance(team.name, str)
    vampytest.assert_instance(team.owner_id, int)


def test__Team__new__0():
    """
    Tests whether ``Team.__new__`` works as intended.
    
    Case: No parameters given.
    """
    team = Team()
    _assert_is_every_attribute_set(team)


def test__Team__new__1():
    """
    Tests whether ``Team.__new__`` works as intended.
    
    Case: All parameters given.
    """
    
    icon = Icon(IconType.static, 2)
    members = [TeamMember(user = User.precreate(202211240000))]
    name = 'Red'
    owner_id = 202211240001
    
    team = Team(
        icon = icon,
        members = members,
        name = name,
        owner_id = owner_id,
    )
    _assert_is_every_attribute_set(team)
    
    vampytest.assert_eq(team.icon, icon)
    vampytest.assert_eq(team.members, tuple(members))
    vampytest.assert_eq(team.name, name)
    vampytest.assert_eq(team.owner_id, owner_id)



def test__Team__create_empty():
    """
    Tests whether ``Team._create_empty`` works as intended.
    """
    team_id = 202211240002
    
    team = Team._create_empty(team_id)
    _assert_is_every_attribute_set(team)
    vampytest.assert_eq(team.id, team_id)


def test__Team__precreate__0():
    """
    Tests whether ``Team.precreate`` works as intended.
    
    Case: No parameters given.
    """
    team_id = 202211240003
    
    team = Team.precreate(team_id)
    _assert_is_every_attribute_set(team)
    vampytest.assert_eq(team.id, team_id)


def test__Team__precreate__1():
    """
    Tests whether ``Team.precreate`` works as intended.
    
    Case: All parameters given.
    """
    team_id = 202211240004
    icon = Icon(IconType.static, 2)
    members = [TeamMember(user = User.precreate(202211240005))]
    name = 'Red'
    owner_id = 202211240006
    
    team = Team.precreate(
        team_id,
        icon = icon,
        members = members,
        name = name,
        owner_id = owner_id,
    )
    _assert_is_every_attribute_set(team)
    vampytest.assert_eq(team.id, team_id)
    
    vampytest.assert_eq(team.icon, icon)
    vampytest.assert_eq(team.members, tuple(members))
    vampytest.assert_eq(team.name, name)
    vampytest.assert_eq(team.owner_id, owner_id)


def test__Team__precreate__2():
    """
    Tests whether ``Team.precreate`` works as intended.
    
    Case: Check caching.
    """
    team_id = 202211240007
    
    team = Team.precreate(team_id)
    test_team = Team.precreate(team_id)
    vampytest.assert_is(team, test_team)
