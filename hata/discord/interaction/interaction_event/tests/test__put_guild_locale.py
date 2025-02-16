import vampytest

from ....localization import Locale

from ..fields import put_guild_locale


def _iter_options():
    yield (
        Locale.czech,
        False,
        {
            'guild_locale': Locale.czech.value,
        },
    )
    
    yield (
        Locale.czech,
        True,
        {
            'guild_locale': Locale.czech.value,
        },
    )
    

@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_guild_locale(input_value, defaults):
    """
    Tests whether ``put_guild_locale`` is working as intended.
    
    Parameters
    ----------
    input_value : ``Locale```
        Value to serialise.
    defaults : `bool`
        Whether fields with their default values should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_guild_locale(input_value, {}, defaults)
