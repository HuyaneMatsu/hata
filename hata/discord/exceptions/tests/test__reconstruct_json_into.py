import vampytest
from scarletio import to_json

from ..payload_renderer import reconstruct_json_into

from .helpers import _assert_list_of_str


def _iter_options():
    yield to_json({'hey': 'mister'}), 0, 50, 0, '{\n    "hey": "mister",\n}'
    yield to_json({'hey': 'mister'}), 1, 50, 0, '{\n        "hey": "mister",\n    }'
    yield 'hey)mister', 0, 50, 0, '"hey)mister"'
    yield 'hey)mister', 0, 50, 50 - 12, '"hey)mister"'
    yield 'hey)mister', 0, 50, 50 - 12 + 1, '(\n    "hey)mister"\n)'
    yield 'hey)mister', 1, 50, 50 - 12 + 1 - 4, '(\n        "hey)mister"\n    )'


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__reconstruct_json_into(input_value, indent, line_width, used_characters):
    """
    Tests whether ``reconstruct_json_into`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to test with.
    indent : `int`
        The amount of indents to add.
    value_is_file : `bool`
        Whether the value is a file and should not be shown.
    line_width : `int`
        Allowed line width.
    used_characters : `int`
        The amount of used characters.
    
    Returns
    -------
    output : `str`
    """
    into = reconstruct_json_into(input_value, [], indent, line_width, used_characters)
    
    _assert_list_of_str(into)
    
    return ''.join(into)
