import vampytest

from ..fields import parse_choice_index


def _iter_options():
    yield (
        {},
        -1,
    )
    
    yield (
        {
            'response': None,
        },
        -1,
    )
    
    yield (
        {
            'response': 1,
        },
        1,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_choice_index(input_data):
    output = parse_choice_index(input_data)
    vampytest.assert_instance(output, int)
    return output
