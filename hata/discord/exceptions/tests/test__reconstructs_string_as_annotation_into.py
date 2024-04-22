import vampytest

from ..payload_renderer import _reconstruct_string_as_annotation_into

from .helpers import _assert_list_of_str


def _iter_options():
    # Default
    yield (
        'hey mister',
        0,
        50,
        0,
        'String<length = 10>',
    )
    
    # Just enough space
    yield (
        'hey mister',
        0,
        50,
        50 - 19,
        'String<length = 10>',
    )
    
    # Just enough space + indent
    yield (
        'hey mister',
        1,
        50,
        50 - 19 - 4,
        'String<length = 10>',
    )
    
    # Not enough space
    yield (
        'hey mister',
        0,
        50,
        50 - 19 + 1,
        (   
            '(\n'
            '    String<length = 10>\n'
            ')'
        ),
    )
    
    # Not enough space + indent
    yield (
        'hey mister',
        1,
        50,
        50 - 19 - 4 + 1,
        (   
            '(\n'
            '        String<length = 10>\n'
            '    )'
        ),
    )

@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__reconstruct_string_as_annotation_into(input_value, indent, line_width, used_characters):
    """
    Tests whether ``_reconstruct_string_as_annotation_into`` works as intended.
    
    Parameters
    ----------
    input_value : `str`
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
    into = _reconstruct_string_as_annotation_into(input_value, [], indent, line_width, used_characters)
    
    _assert_list_of_str(into)
    
    return ''.join(into)
