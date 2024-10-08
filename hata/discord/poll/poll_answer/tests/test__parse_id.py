import vampytest

from ..fields import parse_id


def _iter_options():
    answer_id = 202404130005
    
    yield {}, 0
    yield {'answer_id': None}, 0
    yield {'answer_id': str(answer_id)}, answer_id


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_id(input_data):
    """
    Tests whether ``parse_id`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `int`
    """
    output = parse_id(input_data)
    vampytest.assert_instance(output, int)
    return output
