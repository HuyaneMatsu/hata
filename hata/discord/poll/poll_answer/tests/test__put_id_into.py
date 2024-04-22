import vampytest

from ..fields import put_id_into


def _iter_options():
    answer_id = 202404130006
    
    yield 0, False, {'answer_id': None}
    yield 0, True, {'answer_id': None}
    yield answer_id, False, {'answer_id': str(answer_id)}
    yield answer_id, True, {'answer_id': str(answer_id)}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_id_into(input_value, defaults):
    """
    Tests whether ``put_id_into`` works as intended.
    
    Parameters
    ----------
    input_value : `int`
        The value to serialise.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_id_into(input_value, {}, defaults)
