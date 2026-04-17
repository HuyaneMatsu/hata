import vampytest

from ...poll_result import PollResult

from ..fields import put_results


def _iter_options():
    result_0 = PollResult(answer_id = 202404140016)
    result_1 = PollResult(answer_id = 202404140017)
    
    yield (
        None,
        False,
        {
            'results': {
                'answer_counts': [],
            },
        },
    )
    
    yield (
        None,
        True,
        {
            'results': {
                'answer_counts': [],
            },
        },
    )
    
    yield (
        [result_0, result_1],
        False,
        {
            'results': {
                'answer_counts': [
                    result_0.to_data(defaults = False),
                    result_1.to_data(defaults = False),
                ],
            },
        },
    )
    
    yield (
        [result_0, result_1],
        True,
        {
            'results': {
                'answer_counts': [
                    result_0.to_data(defaults = True),
                    result_1.to_data(defaults = True),
                ],
            },
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_results(input_value, defaults):
    """
    Tests whether ``put_results`` works as intended.
    
    Parameters
    ----------
    input_value : `None | list<PollResult>`
        Value to serialise.
    defaults : `bool`
        Whether fields with their default values should be included as well.
    
    Returns
    -------    
    output : `dict<str, object>`
    """
    return put_results(input_value, {}, defaults)
