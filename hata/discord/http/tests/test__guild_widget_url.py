import vampytest

from ...guild import Guild

from ..urls import API_ENDPOINT, guild_widget_url


def _iter_options():
    guild_id = 202504160100
    yield (
        guild_id,
        f'{API_ENDPOINT}/guilds/{guild_id}/widget.png?style=shield',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__guild_widget_url(guild_id):
    """
    Tests whether ``guild_widget_url`` works as intended.
    
    Parameters
    ----------
    guild_id : `int`
        Guild identifier to create guild for.
    
    Returns
    -------
    output : `None | str`
    """
    guild = Guild.precreate(guild_id)
    output = guild_widget_url(guild)
    vampytest.assert_instance(output, str, nullable = True)
    return output
