import vampytest

from ..fields_common import parse_title__from_label


def _iter_options():
    yield (
        {},
        None,
    )
    
    yield (
        {
            'label': None,
        },
        None,
    )
    
    yield (
        {
            'label': '',
        },
        None,
    )
    
    yield (
        {
            'label': 'a',
        },
        'a',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_title__from_label(input_data):
    output = parse_title__from_label(input_data)
    vampytest.assert_instance(output, str, nullable = True)
    return output
