import vampytest

from ..payload_renderer import reconstruct_float_into

from .helpers import _assert_list_of_str


def _iter_options():
    yield (
        0.0,
        0,
        50,
        0,
        '0.0'
    )
    
    yield (
        100.5,
        0,
        50,
        0,
        '100.5',
    )
    
    yield (
        -100.5,
        0,
        50,
        0,
        '-100.5',
    )

    # Just not too long
    yield (
        10.0,
        0,
        50,
        50 - 4,
        '10.0',
    )

    # too long
    yield (
        10.0,
        0,
        50,
        50 - 4 + 1,
        (
            '(\n'
            '    10.0\n'
            ')'
        ),
    )

    # too long + indent
    yield (
        10.0,
        1,
        50,
        50 - 4 + 1 - 4,
        (
            '(\n'
            '        10.0\n'
            '    )'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__reconstruct_float_into(input_value, indent, line_width, used_characters):
    """
    Tests whether ``reconstruct_float_into`` works as intended.
    
    Parameters
    ----------
    input_value : `float`
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
    into = reconstruct_float_into(input_value, [], indent, line_width, used_characters)
    
    _assert_list_of_str(into)
    
    return ''.join(into)
