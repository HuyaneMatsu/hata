import vampytest

from ..fields import parse_value


def _iter_options():
    yield (
        {},
        None,
    )
    
    yield (
        {
            'response': None,
        },
        None,
    )
    
    yield (
        {
            'response': '',
        },
        None,
    )
    
    yield (
        {
            'response': 'a',
        },
        'a',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_value(input_data):
    output = parse_value(input_data)
    vampytest.assert_instance(output, str, nullable = True)
    return output
