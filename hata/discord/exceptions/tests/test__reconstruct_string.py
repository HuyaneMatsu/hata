import vampytest

from ..payload_renderer import reconstruct_string


def _iter_options():
    yield 'hey mister', 0, False, 50, 0, '"hey mister"'
    yield 'hey mister', 4, False, 50, 0, '"hey mister"'
    yield 'hey mister', 0, True, 50, 0, 'String<length = 10>'
    yield 'hey mister', 4, True, 50, 0, 'String<length = 10>'
    
    yield (
        'Hey mister do you want to see new year fireworks together?',
        0,
        False,
        50,
        0,
        (
            '(\n'
            '    "Hey mister do you want to see new year firew"\n'
            '    "orks together?"\n'
            ')'
        ),
    )
    
    yield (
        'Hey mister do you want to see new year fireworks together?',
        5,
        False,
        50,
        0,
        (
            '(\n'
            '                        "Hey mister do you want to see new year"\n'
            '                        " fireworks together?"\n'
            '                    )'
        ),
    )
    yield (
        'hey mister', 
        0,
        False,
        50,
        40, 
        (
            '(\n'
            '    "hey mister"\n'
            ')'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__reconstruct_string(input_value, indent, value_is_file, line_width, used_characters):
    """
    Tests whether ``reconstruct_string`` works as intended.
    
    Parameters
    ----------
    input_value : `str`
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
    output = reconstruct_string(input_value, indent, value_is_file, line_width, used_characters)
    vampytest.assert_instance(output, str)
    return output
