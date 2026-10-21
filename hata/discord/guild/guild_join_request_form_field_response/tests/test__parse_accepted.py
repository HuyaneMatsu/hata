import vampytest

from ..fields import parse_accepted


def _iter_options():
    yield (
        {},
        True,
    )
    
    yield (
        {
            'response': False,
        },
        False,
    )
    
    yield (
        {
            'response': True
        },
        True,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_accepted(input_data):
    output = parse_accepted(input_data)
    vampytest.assert_instance(output, bool)
    return output
