import vampytest

from ..fields_common import put_required


def _iter_options():
    yield (
        False,
        False,
        {
            'required': False,
        },
    )
    
    yield (
        True,
        False,
        {
            'required': True,
        },
    )
    
    yield (
        False,
        True,
        {
            'required': False,
        },
    )
    
    yield (
        True,
        True,
        {
            'required': True,
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_required(input_value, defaults):
    return put_required(input_value, {}, defaults)
