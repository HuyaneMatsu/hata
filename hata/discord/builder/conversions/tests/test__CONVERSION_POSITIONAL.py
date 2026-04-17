import vampytest

from ..positional import CONVERSION_POSITIONAL


def _iter_options():
    yield object(), []
    yield None, []
    yield {'hey': 'mister'}, []
    yield ('hey', 'mister'), [('hey', 'mister')]


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__CONVERSION_POSITIONAL__set_identifier(input_value):
    """
    Tests whether ``CONVERSION_POSITIONAL.set_identifier`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to test.
    
    Returns
    -------
    output : `list<tuple<object>>`
    """
    return [*CONVERSION_POSITIONAL.set_identifier(input_value)]
