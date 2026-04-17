import vampytest

from ..urls import API_ENDPOINT, build_guild_widget_url_as


def _iter_options():
    guild_id = 202405170110
    
    yield (
        guild_id,
        'shield',
        f'{API_ENDPOINT}/guilds/{guild_id}/widget.png?style=shield',
    )
    
    yield (
        guild_id,
        'banner1',
        f'{API_ENDPOINT}/guilds/{guild_id}/widget.png?style=banner1',
    )
    
    yield (
        guild_id,
        'banner2',
        f'{API_ENDPOINT}/guilds/{guild_id}/widget.png?style=banner2',
    )
    
    yield (
        guild_id,
        'banner3',
        f'{API_ENDPOINT}/guilds/{guild_id}/widget.png?style=banner3',
    )
    
    yield (
        guild_id,
        'banner4',
        f'{API_ENDPOINT}/guilds/{guild_id}/widget.png?style=banner4',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_guild_widget_url_as(guild_id, style):
    """
    Tests whether ``build_guild_widget_url_as`` works as intended.
    
    Parameters
    ----------
    guild_id : `int`
        Guild identifier to test with.
        
    style : `str`
        The widget image's style.
    
    Returns
    -------
    output : `str`
    """
    output = build_guild_widget_url_as(guild_id, style)
    vampytest.assert_instance(output, str)
    return output
