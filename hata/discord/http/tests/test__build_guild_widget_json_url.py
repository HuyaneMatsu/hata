import vampytest

from ..urls import API_ENDPOINT, build_guild_widget_json_url


def _iter_options():
    guild_id = 202504160120
    yield (
        guild_id,
        f'{API_ENDPOINT}/guilds/{guild_id}/widget.json',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_guild_widget_json_url(guild_id):
    """
    Tests whether ``build_guild_widget_json_url`` works as intended.
    
    Parameters
    ----------
    guild_id : `int`
        Guild identifier to test with.
    
    Returns
    -------
    output : `None | str`
    """
    output = build_guild_widget_json_url(guild_id)
    vampytest.assert_instance(output, str, nullable = True)
    return output
