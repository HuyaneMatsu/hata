import vampytest

from ..fields_common import parse_title


def _iter_options():
    yield (
        {},
        None,
    )
    
    yield (
        {
            'title': None,
        },
        None,
    )
    
    yield (
        {
            'title': '',
        },
        None,
    )
    
    yield (
        {
            'title': 'a',
        },
        'a',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_title(input_data):
    output = parse_title(input_data)
    vampytest.assert_instance(output, str, nullable = True)
    return output
