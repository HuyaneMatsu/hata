import vampytest

from ..urls import is_cdn_url


def _iter_options():
    yield (
        'https://cdn.discordapp.com/miau',
        True,
    )
    yield (
        'https://discord.com/miau',
        True,
    )
    yield (
        'https://canary.discord.com/miau',
        True,
    )
    yield (
        'https://ptb.discord.com/miau',
        True,
    )
    yield (
        'https://images-ext-1.discordapp.net/miau',
        True,
    )
    yield (
        'https://images-ext-200.discordapp.net/miau',
        True,
    )
    yield (
        'https://media.discordapp.net/miau',
        True,
    )
    yield (
        'https://discord.gg/houjuu_nue',
        False,
    )
    yield (
        'https://orindance.party/miau',
        False,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__is_cdn_url(url):
    """
    Tests whether ``is_cdn_url`` works as intended.
    
    Parameters
    ----------
    url : `str`
        The url to check.
    
    Returns
    -------
    output : `bool`
    """
    output = is_cdn_url(url)
    vampytest.assert_instance(output, bool)
    return output
