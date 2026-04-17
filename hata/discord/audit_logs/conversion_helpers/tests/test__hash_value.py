import vampytest

from ..helpers import _hash_change_value


def _iter_options():
    yield None
    yield 7
    yield {2: 3, 5: 7}


@vampytest.call_from(_iter_options())
def test__hash_change_value(value):
    """
    Tests whether ``_hash_change_value`` works as intended.
    
    Parameters
    ----------
    value : `object`
        The value to hash.
    """
    output = _hash_change_value(value)
    vampytest.assert_instance(output, int)
