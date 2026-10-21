import vampytest

from ..fields_common import put_title__to_label


def _iter_options():
    yield (
        None,
        False,
        {
            'label': '',
        },
    )
    
    yield (
        None,
        True,
        {
            'label': '',
        },
    )
    
    yield (
        'a',
        False,
        {
            'label': 'a',
        },
    )
    
    yield (
        'a',
        True,
        {
            'label': 'a',
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_title__to_label(input_value, defaults):
    return put_title__to_label(input_value, {}, defaults)
