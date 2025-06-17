import vampytest

from ...bases import IconType

from ..urls import CDN_ENDPOINT, build_team_icon_url_as


def _iter_options():
    team_id = 202504170130
    yield (
        team_id,
        IconType.none,
        0,
        None,
        None,
        None,
    )
    
    team_id = 202504170131
    yield (
        team_id,
        IconType.static,
        2,
        None,
        1024,
        f'{CDN_ENDPOINT}/team-icons/{team_id}/00000000000000000000000000000002.png?size=1024',
    )
    
    team_id = 202504170132
    yield (
        team_id,
        IconType.animated,
        3,
        None,
        None,
        f'{CDN_ENDPOINT}/team-icons/{team_id}/a_00000000000000000000000000000003.gif',
    )
    
    team_id = 202504170133
    yield (
        team_id,
        IconType.animated,
        3,
        'png',
        None,
        f'{CDN_ENDPOINT}/team-icons/{team_id}/a_00000000000000000000000000000003.png',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_team_icon_url_as(team_id, icon_type, icon_hash, ext, size):
    """
    Tests whether ``build_team_icon_url_as`` works as intended.
    
    Parameters
    ----------
    team_id : `int`
        Team identifier to test with.
    
    icon_type : ``IconType``
        The icon's type.
    
    icon_hash : `int`
        The icon's hash (uint128).
    
    ext : `None | str`
        The extension of the image's url.
    
    size : `None | int`
        The preferred minimal size of the image's url.
    
    Returns
    -------
    output : `None | str`
    """
    output = build_team_icon_url_as(team_id, icon_type, icon_hash, ext, size)
    vampytest.assert_instance(output, str, nullable = True)
    return output
