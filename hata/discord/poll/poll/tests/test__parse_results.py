import vampytest

from ....user import User

from ...poll_result import PollResult

from ..fields import parse_results


def _iter_options():
    result_0 = PollResult(answer_id = 202404140012)
    result_1 = PollResult(answer_id = 202404140013)
    result_2 = PollResult(answer_id = 202404170000, count = 4, users = [User.precreate(202404170001)])
    result_3 = PollResult(answer_id = 202404170000, count = 4)
    
    yield {}, None, None
    yield {'results': None}, None, None
    yield {'results': {}}, None, None
    yield {'results': {'answer_counts': None}}, None, None
    yield {'results': {'answer_counts': []}}, None, None
    yield (
        {
            'results': {
                'answer_counts': [
                   result_0.to_data(defaults = True),
                ],
            },
        },
        None,
        [result_0],
    )
    yield (
        {
            'results': {
                'answer_counts': [
                    result_0.to_data(defaults = True),
                    result_1.to_data(defaults = True),
                ],
            },
        },
        None,
        [result_0, result_1],
    )
    yield (
        {
            'results': {
                'answer_counts': [
                    result_1.to_data(defaults = True),
                    result_0.to_data(defaults = True),
                ],
            },
        },
        None,
        [result_1, result_0],
    )
    
    # with old result.
    yield (
        {
            'results': {
                'answer_counts': [
                    result_3.to_data(defaults = True),
                ],
            },
        },
        [result_2],
        [result_2],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_results(input_data, old_results):
    """
    Tests whether ``parse_results`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    old_results : `None | list<PollResult>` = `None`, Optional
        Old results of the poll.
    
    Returns
    -------
    output : `none | list<PollResult>`
    """
    if (old_results is not None):
        old_results = [result.copy() for result in old_results]
    
    return parse_results(input_data, old_results)
