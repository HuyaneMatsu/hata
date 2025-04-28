import vampytest

from ...guild import Guild
from ...utils import is_url

from ..urls import INVITE_ENDPOINT, guild_vanity_invite_url


def _iter_options():
    guild_id = 202504170030
    invite_code = 'tewi'
    yield (
        guild_id,
        invite_code,
        f'{INVITE_ENDPOINT}/{invite_code}',
    )
    
    guild_id = 202504170031
    invite_code = None
    yield (
        guild_id,
        invite_code,
        None,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__guild_vanity_invite_url(guild_id, invite_code):
    """
    Tests whether ``guild_vanity_invite_url`` works as intended.
    
    Parameters
    ----------
    guild_id : `int`
        Guild identifier.
    
    invite_code : `str`
        Code to create the invite with.
    
    Returns
    -------
    output : `None | str`
    """
    guild = Guild.precreate(guild_id, vanity_code = invite_code)
    
    output = guild_vanity_invite_url(guild)
    vampytest.assert_instance(output, str, nullable = True)
    
    if (output is not None):
        vampytest.assert_true(is_url(output))
    
    return output
