import vampytest

from ....user import User

from ..poll_result import PollResult
from ..utils import merge_update_poll_results


def _iter_options():
    user_0 = User.precreate(202404160034)
    user_1 = User.precreate(202404160035)
    
    answer_id_0 = 202404160036
    answer_id_1 = 202404160037
    answer_id_2 = 202404160038
    
    result_0 = PollResult(answer_id = answer_id_0, count = 12, users = [user_0, user_1])
    result_1 = PollResult(answer_id = answer_id_1, count = 2)
    result_2 = PollResult(answer_id = answer_id_2, count = 4)
    result_3 = PollResult(answer_id = answer_id_2, count = 5)
    result_4 = PollResult(answer_id = answer_id_0, count = 12)
    result_5 = PollResult(answer_id = answer_id_0, count = 11)
    
    # No new results
    yield (
        None,
        [result_0, result_1],
        None,
    )
    
    # No old results
    yield (
        [result_1, result_2],
        None,
        [result_1, result_2],
    )
    
    
    # Removed result
    yield (
        [result_0],
        [result_0, result_1],
        [result_0],
    )

    # added result
    yield (
        [result_0, result_2],
        [result_0],
        [result_0, result_2],
    )

    # merged result (count only)
    yield (
        [result_3],
        [result_2],
        [result_3],
    )

    # merged result (user keep)
    yield (
        [result_4],
        [result_0],
        [result_0],
    )

    # merged result (user clean)
    yield (
        [result_5],
        [result_0],
        [result_5],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__merge_update_poll_results(new_results, old_results):
    """
    Tests whether ``merge_update_poll_results`` works as intended.
    
    Parameters
    ----------
    new_results : `None | list<PollResult>`
        New results.
    old_results : `None | list<PollResult>`
        Old results.
    
    Returns
    -------
    results : `None | list<PollResult>`
    """
    if (new_results is not None):
        new_results = [result.copy() for result in new_results]
    
    if (old_results is not None):
        old_results = [result.copy() for result in old_results]
    
    return merge_update_poll_results(new_results, old_results)
