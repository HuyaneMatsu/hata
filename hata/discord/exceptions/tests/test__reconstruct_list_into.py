import vampytest

from ..payload_renderer import reconstruct_list_into

from .helpers import _assert_list_of_str


def _iter_options():
    yield [], 0, 50, '[]'
    yield [], 5, 50, '[]'
    
    yield (
        [None, 56, 'hey mister'],
        0,
        50,
        (
            '[\n'
            '    0: null,\n'
            '    1: 56,\n'
            '    2: "hey mister",\n'
            ']'
        )
    )
    yield (
        [None, 56, 'hey mister'],
        1,
        50,
        (
            '[\n'
            '        0: null,\n'
            '        1: 56,\n'
            '        2: "hey mister",\n'
            '    ]'
        )
    )
    yield (
        ['Hey mister do you want to see new year f'],
        0,
        50,
        (
            '[\n'
            '    0: "Hey mister do you want to see new year f",'
            '\n]'
        )
    )
    yield (
        ['Hey mister do you want to see new year fi'],
        0,
        50,
        (
            '[\n'
            '    0: (\n'
            '        "Hey mister do you want to see new year f"\n'
            '        "i"\n'
            '    ),\n'
            ']'
        )
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__reconstruct_list_into(input_value, indent, line_width):
    """
    Tests whether ``reconstruct_list_into`` works as intended.
    
    Parameters
    ----------
    input_value : `list`
        The value to reconstruct.
    indent : `int`
        The amount of indents to add.
    line_width : `int`
        Allowed line width.
    
    Returns
    -------
    output : `str`
    """
    into = reconstruct_list_into(input_value, [], indent, line_width)
    
    _assert_list_of_str(into)
    
    return ''.join(into)
