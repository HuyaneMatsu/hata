import vampytest

from ....localization import Locale
from ....localization.utils import LOCALE_DEFAULT

from ..fields import parse_guild_locale


def _iter_options():
    yield ({}, LOCALE_DEFAULT)
    yield ({'guild_locale': Locale.czech.value}, Locale.czech)


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_guild_locale(input_data):
    """
    Tests whether ``parse_guild_locale`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        The data to parse from.
    
    Returns
    -------
    output : ``Locale``
    """
    output = parse_guild_locale(input_data)
    vampytest.assert_instance(output, Locale)
    return output
