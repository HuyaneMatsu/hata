import vampytest

from ..payload_renderer import _is_string_length_over


def _iter_options():
    yield 'h', 5, False
    yield '\U0002ffff', 5, True
    yield '\U0001f49a', 5, False
    yield 'hey mister', 5, True
    yield 'hey', 5, False
    yield '\t\t\t', 5, True


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__is_string_length_over(string, length_limit):
    """
    Tests whether ``_is_string_length_over`` works as intended.
    
    Parameters
    ----------
    string : `str`
        Value to test with.
    length_limit : `int`
        Allowed length.
    
    Returns
    -------
    output : `int`
    """
    output = _is_string_length_over(string, length_limit)
    vampytest.assert_instance(output, bool)
    return output
