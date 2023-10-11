import vampytest

from ....localization import Locale

from ..fields import put_user_locale_into


def _iter_options():
    yield (
        Locale.czech,
        False,
        {
            'locale': Locale.czech.value,
        },
    )
    
    yield (
        Locale.czech,
        True,
        {
            'locale': Locale.czech.value,
        },
    )
    

@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_user_locale_into(input_value, defaults):
    """
    Tests whether ``put_user_locale_into`` is working as intended.
    
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
    return put_user_locale_into(input_value, {}, defaults)
