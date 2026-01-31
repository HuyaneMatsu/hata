import vampytest

from ..fields import put_result_count


def _iter_options():
    yield (
        0,
        False,
        {
            'total_results': 0,
        },
    )
    
    yield (
        0,
        True,
        {
            'total_results': 0,
        },
    )
    
    yield (
        1,
        False,
        {
            'total_results': 1,
        },
    )
    
    yield (
        1,
        True,
        {
            'total_results': 1,
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_result_count(result_count, defaults):
    """
    Tests whether ``put_result_count`` works as intended.
    
    Parameters
    ----------
    result_count : `int`
        The result_count to serialise.
    
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_result_count(result_count, {}, defaults)
