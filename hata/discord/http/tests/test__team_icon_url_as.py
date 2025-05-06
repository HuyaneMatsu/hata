import vampytest

from ...application import Team
from ...bases import Icon, IconType

from ..urls import CDN_ENDPOINT, team_icon_url_as


def _iter_options():
    team_id = 202504170130
    yield (
        team_id,
        None,
        {},
        None,
    )
    
    team_id = 202504170131
    yield (
        team_id,
        Icon(IconType.static, 2),
        {'size': 1024},
        f'{CDN_ENDPOINT}/team-icons/{team_id}/00000000000000000000000000000002.png?size=1024',
    )
    
    team_id = 202504170132
    yield (
        team_id,
        Icon(IconType.animated, 3),
        {},
        f'{CDN_ENDPOINT}/team-icons/{team_id}/a_00000000000000000000000000000003.gif',
    )
    
    team_id = 202504170133
    yield (
        team_id,
        Icon(IconType.animated, 3),
        {'ext': 'png'},
        f'{CDN_ENDPOINT}/team-icons/{team_id}/a_00000000000000000000000000000003.png',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__team_icon_url_as(team_id, icon, keyword_parameters):
    """
    Tests whether ``team_icon_url_as`` works as intended.
    
    Parameters
    ----------
    team_id : `int`
        Team identifier to create team for.
    
    icon : `None | Icon`
        Icon to create the team with.
    
    keyword_parameters : `dict<str, object>`
        Additional keyword parameters to pass.
    
    Returns
    -------
    output : `None | str`
    """
    team = Team.precreate(team_id, icon = icon)
    output = team_icon_url_as(team, **keyword_parameters)
    vampytest.assert_instance(output, str, nullable = True)
    return output
