import vampytest

from ..payload_renderer import reconstruct_boolean_into

from .helpers import _assert_list_of_str


def _iter_options():
    yield (
        True,
        0,
        50,
        0,
        'true',
    )
    
    yield (
        False,
        0,
        50,
        0,
        'false',
    )
    
    # just not too long
    yield (
        True,
        0,
        50,
        50 - 4,
        'true',
    )
    
    # too long
    yield (
        True,
        0,
        50,
        50 - 4 + 1,
        (
            '(\n'
            '    true\n'
            ')'
        ),
    )
    
    # too long + indent
    yield (
        True,
        1,
        50,
        50 - 4 + 1 - 4,
        (
            '(\n'
            '        true\n'
            '    )'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__reconstruct_boolean_into(input_value, indent, line_width, used_characters):
    """
    Tests whether ``reconstruct_boolean_into`` works as intended.
    
    Parameters
    ----------
    input_value : `bool`
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
    into = reconstruct_boolean_into(input_value, [], indent, line_width, used_characters)
    
    _assert_list_of_str(into)
    
    return ''.join(into)
