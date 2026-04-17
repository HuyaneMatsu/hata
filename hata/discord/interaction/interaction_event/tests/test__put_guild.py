import vampytest

from ....guild import Guild
from ....localization import Locale

from ..fields import put_guild


def _iter_options():
    yield None, False, {}
    yield None, True, {'guild': None, 'guild_id': None, 'guild_locale': None}
    
    guild_id = 202310100005
    name = 'Remilia'
    
    guild = Guild.precreate(
        guild_id,
        name = name,
    )
    
    expected_output = {
        'guild': {
            'id': str(guild_id),
            'preferred_locale': Locale.english_us.value,
            'locale': Locale.english_us.value,
            'features': [],
        },
        'guild_id': str(guild_id),
        'guild_locale': Locale.english_us.value,
    }
    yield guild, False, expected_output
    
    expected_output = {
        'guild': {
            'id': str(guild_id),
            'preferred_locale': Locale.english_us.value,
            'locale': Locale.english_us.value,
            'features': [],
        },
        'guild_id': str(guild_id),
        'guild_locale': Locale.english_us.value,
    }
    yield guild, True, expected_output


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_guild(guild, defaults):
    """
    Tests whether ``put_guild`` works as intended.
    
    Parameters
    ----------
    guild : `None`, ``Guild``
        The guild to serialise.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_guild(guild, {}, defaults)
