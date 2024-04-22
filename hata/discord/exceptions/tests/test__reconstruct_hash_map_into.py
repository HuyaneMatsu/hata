from collections import OrderedDict

import vampytest

from ..payload_renderer import reconstruct_hash_map_into

from .helpers import _assert_list_of_str


def _iter_options():
    yield OrderedDict(), 0, 50, '{}'
    yield OrderedDict(), 5, 50, '{}'
    
    # generic
    yield (
        {
            'pudding': None,
            'lord': 56,
            'eating': 'hey mister',
        },
        0,
        50,
        (
            '{\n'
            '    "eating": "hey mister",\n'
            '    "lord": 56,\n'
            '    "pudding": null,\n'
            '}'
        )
    )
    
    # generic with indent
    yield (
        {
            'pudding': None,
            'lord': 56,
            'eating': 'hey mister',
        },
        1,
        50,
        (
            '{\n'
            '        "eating": "hey mister",\n'
            '        "lord": 56,\n'
            '        "pudding": null,\n'
            '    }'
        )
    )
    
    # just not too long key + value
    yield (
        {
            'pudding': 'Hey mister do you want to see ne',
        },
        0,
        50,
        (
            '{\n'
            '    "pudding": "Hey mister do you want to see ne",\n'
            '}'
        )
    )
    
    # too long key + value
    yield (
        {
            'pudding': 'Hey mister do you want to see new',
        },
        0,
        50,
        (
            '{\n'
            '    "pudding": (\n'
            '        "Hey mister do you want to see new"\n'
            '    ),\n'
            '}'
        )
    )
    
    # just not too long key + value
    yield (
        {
            'Hey mister do you want to see ne': 'pudding',
        },
        0,
        50,
        (
            '{\n'
            '    "Hey mister do you want to see ne": "pudding",\n'
            '}'
        )
    )
    
    # too long key + value
    yield (
        {
            'Hey mister do you want to see new': 'pudding',
        },
        0,
        50,
        (
            '{\n'
            '    "Hey mister do you want to see new": (\n'
            '        "pudding"\n'
            '    ),\n'
            '}'
        )
    )
    
    # multy line key
    yield (
        {
            'Hey mister do you want to see new year fireworks together?': 'pudding',
        },
        0,
        50,
        (
            '{\n'
            '    (\n'
            '        "Hey mister do you want to see new year f"\n'
            '        "ireworks together?"\n'
            '    ): "pudding",\n'
            '}'
        )
    )
    
    # multy line key, just not too long value
    yield (
        {
            'Hey mister do you want to see new year fireworks together?': 'Hey mister do you want to see new year f',
        },
        0,
        50,
        (
            '{\n'
            '    (\n'
            '        "Hey mister do you want to see new year f"\n'
            '        "ireworks together?"\n'
            '    ): "Hey mister do you want to see new year f",\n'
            '}'
        )
    )
    
    # multy line key, too long value
    yield (
        {
            'Hey mister do you want to see new year fireworks together?': 'Hey mister do you want to see new year fi',
        },
        0,
        50,
        (
            '{\n'
            '    (\n'
            '        "Hey mister do you want to see new year f"\n'
            '        "ireworks together?"\n'
            '    ): (\n'
            '        "Hey mister do you want to see new year f"\n'
            '        "i"\n'
            '    ),\n'
            '}'
        )
    )



@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__reconstruct_hash_map_into(input_value, indent, line_width):
    """
    Tests whether ``reconstruct_hash_map_into`` works as intended.
    
    Parameters
    ----------
    input_value : `dict`
        The value to reconstruct.
    indent : `int`
        The amount of indents to add.
    line_width : `int`
        Allowed line width.
    
    Returns
    -------
    output : `str`
    """
    into = reconstruct_hash_map_into(input_value, [], indent, line_width)
    
    _assert_list_of_str(into)
    
    return ''.join(into)
