import vampytest

from ...guild import Guild

from ..urls import API_ENDPOINT, guild_widget_url_as


def _iter_options():
    guild_id = 202405170110
    yield (
        guild_id,
        {},
        f'{API_ENDPOINT}/guilds/{guild_id}/widget.png?style=shield',
    )
    
    yield (
        guild_id,
        {'style': 'shield'},
        f'{API_ENDPOINT}/guilds/{guild_id}/widget.png?style=shield',
    )
    
    yield (
        guild_id,
        {'style': 'banner1'},
        f'{API_ENDPOINT}/guilds/{guild_id}/widget.png?style=banner1',
    )
    
    yield (
        guild_id,
        {'style': 'banner2'},
        f'{API_ENDPOINT}/guilds/{guild_id}/widget.png?style=banner2',
    )
    
    yield (
        guild_id,
        {'style': 'banner3'},
        f'{API_ENDPOINT}/guilds/{guild_id}/widget.png?style=banner3',
    )
    
    yield (
        guild_id,
        {'style': 'banner4'},
        f'{API_ENDPOINT}/guilds/{guild_id}/widget.png?style=banner4',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__guild_widget_url_as(guild_id, keyword_parameters):
    """
    Tests whether ``guild_widget_url_as`` works as intended.
    
    Parameters
    ----------
    guild_id : `int`
        Guild identifier to create guild for.
    
    keyword_parameters : `dict<str, object>`
        Additional keyword parameters to pass.
    
    Returns
    -------
    output : `None | str`
    """
    guild = Guild.precreate(guild_id)
    output = guild_widget_url_as(guild, **keyword_parameters)
    vampytest.assert_instance(output, str, nullable = True)
    return output
