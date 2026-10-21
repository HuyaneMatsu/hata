import vampytest

from ..fields_common import parse_required


def _iter_options():
    yield (
        {},
        False,
    )
    
    yield (
        {
            'required': None,
        },
        False,
    )
    
    yield (
        {
            'required': False,
        },
        False,
    )
    
    yield (
        {
            'required': True,
        },
        True,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_required(input_data):
    output = parse_required(input_data)
    vampytest.assert_instance(output, bool)
    return output
