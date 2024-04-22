import vampytest

from ..poll_result import PollResult
from ..utils import poll_result_sort_key


def test__poll_result_sort_key():
    """
    Tests whether ``poll_result_sort_key`` works as intended.
    """
    answer_id = 202404170021
    
    poll_result = PollResult(answer_id = answer_id)
    
    sort_key = poll_result_sort_key(poll_result)
    vampytest.assert_instance(sort_key, int)
    vampytest.assert_eq(sort_key, answer_id)
