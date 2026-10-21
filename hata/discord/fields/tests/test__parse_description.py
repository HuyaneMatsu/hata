import vampytest

from ..fields_common import parse_description


def _iter_options():
    yield (
        {},
        None,
    )
    
    yield (
        {
            'description': None,
        },
        None,
    )
    
    yield (
        {
            'description': '',
        },
        None,
    )
    
    yield (
        {
            'description': 'a',
        },
        'a',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_description(input_data):
    output = parse_description(input_data)
    vampytest.assert_instance(output, str, nullable = True)
    return output
