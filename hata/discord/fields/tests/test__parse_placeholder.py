import vampytest

from ..fields_common import parse_placeholder


def _iter_options():
    yield (
        {},
        None,
    )
    
    yield (
        {
            'placeholder': None,
        },
        None,
    )
    
    yield (
        {
            'placeholder': '',
        },
        None,
    )
    
    yield (
        {
            'placeholder': 'a',
        },
        'a',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_placeholder(input_data):
    output = parse_placeholder(input_data)
    vampytest.assert_instance(output, str, nullable = True)
    return output
