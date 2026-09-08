import vampytest

from ....file_type_filter import FileTypeFilter, file_type_filter_create

from ..fields import parse_file_type_filter


def _iter_options():
    yield (
        {},
        None,
    )
    
    yield (
        {
            'file_types': None,
        },
        None,
    )
    
    yield (
        {
            'file_types': ['.png', '.txt'],
        },
        file_type_filter_create(
            individuals = ['png', 'txt'],
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_file_type_filter(data):
    """
    Tests whether ``parse_file_type_filter`` works as intended.
    
    Parameters
    ----------
    data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : ``None | FileTypeFilter``
    """
    output = parse_file_type_filter(data)
    vampytest.assert_instance(output, FileTypeFilter, nullable = True)
    return output
