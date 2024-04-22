import vampytest

from ..payload_renderer import reconstruct_unexpected_into

from .helpers import _assert_list_of_str


def _iter_options():
    yield (
        NotImplemented,
        0,
        50,
        0,
        'Object: NotImplemented',
    )
    
    # just enough space
    yield (
        NotImplemented,
        0,
        50,
        50 - 22,
        'Object: NotImplemented',
    )
    
    # Not enough space
    yield (
        NotImplemented,
        0,
        50,
        50 - 22 + 1,
        (
            '(\n'
            '    Object: NotImplemented\n'
            ')'
        ),
    )
    
    # just enough space + indent
    yield (
        NotImplemented,
        1,
        50,
        50 - 22 - 4,
        'Object: NotImplemented',
    )
    
    # Not enough space + indent
    yield (
        NotImplemented,
        1,
        50,
        50 - 22 + 1 - 4,
        (
            '(\n'
            '        Object: NotImplemented\n'
            '    )'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__reconstruct_unexpected_into(input_value, indent, line_width, used_characters):
    """
    Tests whether ``reconstruct_unexpected_into`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
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
    into = reconstruct_unexpected_into(input_value, [], indent, line_width, used_characters)
    
    _assert_list_of_str(into)
    
    return ''.join(into)
