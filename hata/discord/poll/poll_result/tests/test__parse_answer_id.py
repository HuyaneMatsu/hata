import vampytest

from ..fields import parse_answer_id


def _iter_options():
    answer_id = 202404040000
    
    yield {}, 0
    yield {'id': None}, 0
    yield {'id': str(answer_id)}, answer_id


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_answer_id(input_data):
    """
    Tests whether ``parse_answer_id`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to try to parse the answer identifier from.
    
    Returns
    -------
    output : `int`
    """
    return parse_answer_id(input_data)
