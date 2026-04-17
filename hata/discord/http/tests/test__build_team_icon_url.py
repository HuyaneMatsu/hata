import vampytest

from ...bases import IconType

from ..urls import CDN_ENDPOINT, build_team_icon_url


def _iter_options():
    team_id = 202504170120
    yield (
        team_id,
        IconType.none,
        0,
        None,
    )
    
    team_id = 202504170121
    yield (
        team_id,
        IconType.static,
        2,
        f'{CDN_ENDPOINT}/team-icons/{team_id}/00000000000000000000000000000002.png',
    )
    
    team_id = 202504170122
    yield (
        team_id,
        IconType.animated,
        3,
        f'{CDN_ENDPOINT}/team-icons/{team_id}/a_00000000000000000000000000000003.gif',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_team_icon_url(team_id, icon_type, icon_hash):
    """
    Tests whether ``build_team_icon_url`` works as intended.
    
    Parameters
    ----------
    team_id : `int`
        Team identifier to test with.
    
    icon_type : ``IconType``
        The icon's type.
    
    icon_hash : `int`
        The icon's hash (uint128).
    
    Returns
    -------
    output : `None | str`
    """
    output = build_team_icon_url(team_id, icon_type, icon_hash)
    vampytest.assert_instance(output, str, nullable = True)
    return output
