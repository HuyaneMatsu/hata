import vampytest

from ..flag_meta import _build_duplicate_names_exception_message


def _iter_options():
    yield (
        {
            'koishi': {3, 4},
            'satori': {4, 5},
        },
        (
            'Name: `koishi` has duplicate shifts: 3, 4. '
            'Name: `satori` has duplicate shifts: 4, 5.'
        )
    )
    
    yield (
        {
            'koishi' : {2, 3, 4},
        },
        (
            'Name: `koishi` has duplicate shifts: 2, 3, 4.'
        )
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_duplicate_names_exception_message(shifts_by_name):
    """
    Tests whether ``_build_duplicate_names_exception_message`` works as intended.
    
    Parameters
    ----------
    shifts_by_name : `dict<str, set<int>>`
        The duplicate shifts under the same name.
    
    Returns
    -------
    output : `str`
    """
    output = _build_duplicate_names_exception_message(shifts_by_name)
    vampytest.assert_instance(output, str)
    return output
