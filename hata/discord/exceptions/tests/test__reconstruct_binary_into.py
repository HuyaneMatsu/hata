import vampytest

from ..payload_renderer import reconstruct_binary_into

from .helpers import _assert_list_of_str


def _iter_options():
    yield (
        b'',
        0,
        50,
        0,
        'Binary<length = 0>'
    )
    
    yield (
        b'pudding',
        0,
        50,
        0,
        'Binary<length = 7>',
    )
    
    # just enough space
    yield (
        b'hey mister',
        0,
        50,
        50 - 19 - 4,
        'Binary<length = 10>',
    )
    
    # Just enough space + indent
    yield (
        b'hey mister',
        1,
        50,
        50 - 19 - 4,
        'Binary<length = 10>',
    )
    
    # Not enough space
    yield (
        b'hey mister',
        0,
        50,
        50 - 19 + 1,
        (   
            '(\n'
            '    Binary<length = 10>\n'
            ')'
        ),
    )
    
    # Not enough space + indent
    yield (
        b'hey mister',
        1,
        50,
        50 - 19 - 4 + 1,
        (   
            '(\n'
            '        Binary<length = 10>\n'
            '    )'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__reconstruct_binary_into(input_value, indent, line_width, used_characters):
    """
    Tests whether ``reconstruct_binary_into`` works as intended.
    
    Parameters
    ----------
    input_value : `bytes`
        The value to reconstruct.
    indent : `int`
        The amount of indents to add.
    line_width : `int`
        Allowed line width.
    used_characters : `int`
        The amount of used characters.
    
    Returns
    -------
    output : `str`
    """
    into = reconstruct_binary_into(input_value, [], indent, line_width, used_characters)
    
    _assert_list_of_str(into)
    
    return ''.join(into)
