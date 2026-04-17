import vampytest

from ..payload_renderer import reconstruct_null_into

from .helpers import _assert_list_of_str


def _iter_options():
    yield (
        0,
        50,
        0,
        'null',
    )
    
    # just not too long
    yield (
        0,
        50,
        50 - 4,
        'null',
    )
    
    # too long
    yield (
        0,
        50,
        50 - 4 + 1,
        (
            '(\n'
            '    null\n'
            ')'
        ),
    )
    
    # too long + indent
    yield (
        1,
        50,
        50 - 4 + 1 - 4,
        (
            '(\n'
            '        null\n'
            '    )'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__reconstruct_null_into(indent, line_width, used_characters):
    """
    Tests whether ``reconstruct_null_into`` works as intended.
    
    Parameters
    ----------
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
    into = reconstruct_null_into([], indent, line_width, used_characters)
    
    _assert_list_of_str(into)
    
    return ''.join(into)
