import vampytest

from ..payload_renderer import _reconstruct_string_as_multi_line_into

from .helpers import _assert_list_of_str


def _iter_options():
    yield (
        'Hey mister do you want to see new year fireworks together?',
        0,
        50,
        (
            '(\n'
            '    "Hey mister do you want to see new year firew"\n'
            '    "orks together?"\n'
            ')'
        ),
    )
    yield (
        'Hey mister do you want to see new year fireworks together?\nHey mister, do you want to have a better future?',
        5,
        40,
        (
            '(\n'
            '                        "Hey mister do you want to see new year"\n'
            '                        " fireworks together?\\nHey mister, do y"\n'
            '                        "ou want to have a better future?"\n'
            '                    )'
        ),
    )
    yield (
        'a' + '\t' * 40,
        0,
        50,
        (
            '(\n'
            '    "a\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t"\n'
            '    "\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t"\n'
            ')'
        ),
    )

@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__reconstruct_string_as_multi_line_into(input_value, indent, line_width):
    """
    Tests whether ``_reconstruct_string_as_multi_line_into`` works as intended.
    
    Parameters
    ----------
    input_value : `str`
        The value to reconstruct.
    indent : `int`
        The amount of indents to add.
    line_width : `int`
        Allowed line width.
    
    Returns
    -------
    output : `str`
    """
    into = _reconstruct_string_as_multi_line_into(input_value, [], indent, line_width)
    
    _assert_list_of_str(into)
    
    return ''.join(into)
