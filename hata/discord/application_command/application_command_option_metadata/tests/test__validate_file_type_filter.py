import vampytest

from ....file_type_filter import FileTypeFilter, file_type_filter_create

from ..fields import validate_file_type_filter


def _iter_options():
    yield (
        None,
        None,
    )
    
    yield (
        file_type_filter_create(
            individuals = ['png', 'txt'],
        ),
        file_type_filter_create(
            individuals = ['png', 'txt'],
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__validate_file_type_filter(input_value):
    """
    Tests whether ``validate_file_type_filter`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Returns
    -------
    output : ``None | FileTypeFilter``
    """
    output = validate_file_type_filter(input_value)
    vampytest.assert_instance(output, FileTypeFilter, nullable = True)
    return output
