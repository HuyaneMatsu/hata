import vampytest

from ....file_type_filter import FileTypeFilter, file_type_filter_create

from ..fields import put_file_type_filter


def _iter_options():
    yield (
        None,
        False,
        {},
    )

    yield (
        None,
        True,
        {
            'file_types': None,
        },
    )
    
    yield (
        file_type_filter_create(
            individuals = ['png', 'txt'],
        ),
        False,
        {
            'file_types': ['.png', '.txt'],
        },
    )
    
    yield (
        file_type_filter_create(
            individuals = ['png', 'txt'],
        ),
        True,
        {
            'file_types': ['.png', '.txt'],
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_file_type_filter(input_value, defaults):
    """
    Tests whether ``put_file_type_filter`` works as intended.
    
    Parameters
    ----------
    input_value : ``None | FileTypeFilter``
        Value to serialise.
    
    defaults : `bool`
        Whether values as their defaults should be serialised as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_file_type_filter(input_value, {}, defaults)
