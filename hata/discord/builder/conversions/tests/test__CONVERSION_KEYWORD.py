import vampytest

from ..keyword import CONVERSION_KEYWORD


def _iter_options():
    yield object(), []
    yield None, []
    yield {'hey': 'mister'}, [{'hey': 'mister'}]
    yield ('hey', 'mister'), []


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__CONVERSION_KEYWORD__set_identifier(input_value):
    """
    Tests whether ``CONVERSION_KEYWORD.set_identifier`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to test.
    
    Returns
    -------
    output : `list<dict<str, object>>`
    """
    return [*CONVERSION_KEYWORD.set_identifier(input_value)]
