import vampytest

from ...application import Team
from ...bases import Icon, IconType

from ..urls import CDN_ENDPOINT, team_icon_url


def _iter_options():
    team_id = 202504170120
    yield (
        team_id,
        None,
        None,
    )
    
    team_id = 202504170121
    yield (
        team_id,
        Icon(IconType.static, 2),
        f'{CDN_ENDPOINT}/team-icons/{team_id}/00000000000000000000000000000002.png',
    )
    
    team_id = 202504170122
    yield (
        team_id,
        Icon(IconType.animated, 3),
        f'{CDN_ENDPOINT}/team-icons/{team_id}/a_00000000000000000000000000000003.gif',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__team_icon_url(team_id, icon):
    """
    Tests whether ``team_icon_url`` works as intended.
    
    Parameters
    ----------
    team_id : `int`
        Team identifier to create team for.
    
    icon : `None | Icon`
        Icon to create the team with.
    
    Returns
    -------
    output : `None | str`
    """
    team = Team.precreate(team_id, icon = icon)
    output = team_icon_url(team)
    vampytest.assert_instance(output, str, nullable = True)
    return output
