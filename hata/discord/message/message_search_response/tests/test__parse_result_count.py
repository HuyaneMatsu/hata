import vampytest

from ..fields import parse_result_count


def _iter_options():
    yield (
        {},
        0,
    )
    
    yield (
        {
            'total_results': None,
        },
        0,
    )
    
    yield (
        {
            'total_results': 1,
        },
        1,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_result_count(input_data):
    """
    Tests whether ``parse_result_count`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `int`
    """
    output = parse_result_count(input_data)
    vampytest.assert_instance(output, int)
    return output
