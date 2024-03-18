import vampytest

from ..none import CONVERSION_NONE


def _iter_options():
    yield object(), []
    yield None, [None]
    yield {'hey': 'mister'}, []
    yield ('hey', 'mister'), []


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__CONVERSION_NONE__set_identifier(input_value):
    """
    Tests whether ``CONVERSION_NONE.set_identifier`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to test.
    
    Returns
    -------
    output : `list<None>`
    """
    return [*CONVERSION_NONE.set_identifier(input_value)]
