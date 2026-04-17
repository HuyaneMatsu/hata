import vampytest
from scarletio.web_common import FormData

from ..payload_renderer import reconstruct_form_data_into

from .helpers import _assert_list_of_str


def _iter_options():
    # empty
    form_data_0 = FormData()
    
    yield (
        form_data_0,
        50,
        (
            'FormData()'
        ),
    )
    
    # binary file -> file_name is None
    form_data_1 = FormData()
    form_data_1.add_field('hey', b'mister')
    
    yield (
        form_data_1,
        50,
        (
            'FormData({\n'
            '    0: "hey": Binary<length = 6>,\n'
            '})'
        ),
    )
    
    # binary file -> name == file_name
    form_data_2 = FormData()
    form_data_2.add_field('hey', b'mister', file_name = 'hey')
    
    yield (
        form_data_2,
        50,
        (
            'FormData({\n'
            '    0: "hey": Binary<length = 6>,\n'
            '})'
        ),
    )
    
    # binary file -> name != file_name
    form_data_3 = FormData()
    form_data_3.add_field('hey', b'mister', file_name = 'remilia')
    
    yield (
        form_data_3,
        50,
        (
            'FormData({\n'
            '    0: "hey" | "remilia": Binary<length = 6>,\n'
            '})'
        ),
    )
    
    # string file
    form_data_4 = FormData()
    form_data_4.add_field('hey', 'mister')
    
    yield (
        form_data_4,
        50,
        (
            'FormData({\n'
            '    0: "hey": String<length = 6>,\n'
            '})'
        ),
    )
    
    # string json
    form_data_5 = FormData()
    form_data_5.add_json('hey', 'mister')
    
    yield (
        form_data_5,
        50,
        (
            'FormData({\n'
            '    0: "hey": "mister",\n'
            '})'
        ),
    )
    
    # actual json
    form_data_6 = FormData()
    form_data_6.add_json('hey', {'pudding': 'eater'})
    
    yield (
        form_data_6,
        50,
        (
            'FormData({\n'
            '    0: "hey": {\n'
            '        "pudding": "eater",\n'
            '    },\n'
            '})'
        ),
    )
    
    # multiple values
    form_data_7 = FormData()
    form_data_7.add_field('hey', 'mister')
    form_data_7.add_field('pudding', 'eater')
    
    yield (
        form_data_7,
        50,
        (
            'FormData({\n'
            '    0: "hey": String<length = 6>,\n'
            '    1: "pudding": String<length = 5>,\n'
            '})'
        ),
    )
    
    # name is too long
    form_data_8 = FormData()
    form_data_8.add_field('Hey mister do you want to see new year fi', 'mister')
    
    yield (
        form_data_8,
        50,
        (
            'FormData({\n'
            '    0: (\n'
            '        "Hey mister do you want to see new year f"\n'
            '        "i"\n'
            '    ): String<length = 6>,\n'
            '})'
        ),
    )
    
    # name not long enough
    form_data_9 = FormData()
    form_data_9.add_field('Hey mister do you want to see new year f', 'mister')
    
    yield (
        form_data_9,
        50,
        (
            'FormData({\n'
            '    0: "Hey mister do you want to see new year f": (\n'
            '        String<length = 6>\n'
            '    ),\n'
            '})'
        ),
    )
    
    # file name is too long
    form_data_10 = FormData()
    form_data_10.add_field('hey', 'mister', file_name = 'Hey mister do you want to see n')
    
    yield (
        form_data_10,
        50,
        (
            'FormData({\n'
            '    0: "hey" | (\n'
            '        "Hey mister do you want to see n"\n'
            '    ): String<length = 6>,\n'
            '})'
        ),
    )
    
    # file name not long enough
    form_data_11 = FormData()
    form_data_11.add_field('hey', 'mister', file_name = 'Hey mister do you want to see ')
    
    yield (
        form_data_11,
        50,
        (
            'FormData({\n'
            '    0: "hey" | "Hey mister do you want to see ": (\n'
            '        String<length = 6>\n'
            '    ),\n'
            '})'
        ),
    )
    
    # name and file name is too long
    form_data_12 = FormData()
    form_data_12.add_field(
        'Hey mister, have you seen my sister? Hey mister!!!',
        'mister',
        file_name = 'Hey mister do you want to see new year fireworks together?',
    )
    
    yield (
        form_data_12,
        50,
        (
            'FormData({\n'
            '    0: (\n'
            '        "Hey mister, have you seen my sister? Hey"\n'
            '        " mister!!!"\n'
            '    ) | (\n'
            '        "Hey mister do you want to see new year f"\n'
            '        "ireworks together?"\n'
            '    ): String<length = 6>,\n'
            '})'
        ),
    )
    # name and file name together is too long
    form_data_13 = FormData()
    form_data_13.add_field('Hey mister, have you', 'mister', file_name = 'seen my',)
    
    yield (
        form_data_13,
        50,
        (
            'FormData({\n'
            '    0: "Hey mister, have you" | "seen my": (\n'
            '        String<length = 6>\n'
            '    ),\n'
            '})'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__reconstruct_form_data_into(input_value, line_width):
    """
    Tests whether ``reconstruct_form_data_into`` works as intended.
    
    Parameters
    ----------
    input_value : `FormData`
        The value to reconstruct.
    line_width : `int`
        Allowed line width.
    
    Returns
    -------
    output : `str`
    """
    into = reconstruct_form_data_into(input_value, [], line_width)
    
    _assert_list_of_str(into)
    
    return ''.join(into)
