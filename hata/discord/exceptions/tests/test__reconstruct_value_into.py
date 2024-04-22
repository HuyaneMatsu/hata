import vampytest

from ..payload_renderer import reconstruct_value_into

from .helpers import _assert_list_of_str


def _iter_options():
    yield None, 0, False, 50, 0, 'null'
    yield True, 0, False, 50, 0, 'true'
    yield False, 0, False, 50, 0, 'false'
    yield 'hey mister', 0, False, 50, 0, '"hey mister"'
    yield 'hey mister', 0, True, 50, 0, 'String<length = 10>'
    yield 10, 0, False, 50, 0, '10'
    yield 10.0, 0, False, 50, 0, '10.0'
    yield ['mister'], 0, False, 50, 0, '[\n    0: "mister",\n]'
    yield ['mister'], 1, False, 50, 0, '[\n        0: "mister",\n    ]'
    yield {'hey': 'mister'}, 0, False, 50, 0, '{\n    "hey": "mister",\n}'
    yield {'hey': 'mister'}, 1, False, 50, 0, '{\n        "hey": "mister",\n    }'
    yield b'hey mister', 0, False, 50, 0, 'Binary<length = 10>'
    yield {'mister'}, 0, False, 50, 0, '[\n    0: "mister",\n]'
    yield {'mister'}, 1, False, 50, 0, '[\n        0: "mister",\n    ]'
    yield NotImplemented, 0, False, 50, 0, 'Object: NotImplemented'


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__reconstruct_value_into(input_value, indent, value_is_file, line_width, used_characters):
    """
    Tests whether ``reconstruct_value_into`` works as intended.
    
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
    into = reconstruct_value_into(input_value, [], indent, value_is_file, line_width, used_characters)
    
    _assert_list_of_str(into)
    
    return ''.join(into)
