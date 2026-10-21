import vampytest

from ..fields import parse_total


def _iter_options():
    yield (
        {},
        0,
    )
    
    yield (
        {
            'total': None,
        },
        0,
    )
    
    yield (
        {
            'total': 1,
        },
        1,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_total(input_data):
    output = parse_total(input_data)
    vampytest.assert_instance(output, int)
    return output
