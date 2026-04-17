import vampytest

from ..urls import INVITE_ENDPOINT, build_guild_vanity_invite_url


def _iter_options():
    invite_code = 'tewi'
    
    yield (
        invite_code,
        f'{INVITE_ENDPOINT}/{invite_code}',
    )
    
    invite_code = None
    yield (
        invite_code,
        None,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_guild_vanity_invite_url(vanity_code):
    """
    Tests whether ``build_guild_vanity_invite_url`` works as intended.
    
    Parameters
    ----------
    vanity_code : `None | str`
        The guild's vanity invite core.
    
    Returns
    -------
    output : `None | str`
    """
    output = build_guild_vanity_invite_url(vanity_code)
    vampytest.assert_instance(output, str, nullable = True)
    
    return output
