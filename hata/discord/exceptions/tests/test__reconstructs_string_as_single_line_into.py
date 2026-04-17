import vampytest

from ..payload_renderer import _reconstruct_string_as_single_line_into

from .helpers import _assert_list_of_str


def _iter_options():
    yield 'hey mister', '\"hey mister\"'
    yield '', '\"\"'
    yield '\U0002ffff', '"\\U0002ffff"'
    yield '\U0001f49a', '"\U0001f49a"'


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__reconstruct_string_as_single_line_into(input_value):
    """
    Tests whether ``_reconstruct_string_as_single_line_into`` works as intended.
    
    Parameters
    ----------
    input_value : `str`
        The value to reconstruct.
    
    Returns
    -------
    output : `str`
    """
    into = _reconstruct_string_as_single_line_into(input_value, [])
    
    _assert_list_of_str(into)
    
    return ''.join(into)
