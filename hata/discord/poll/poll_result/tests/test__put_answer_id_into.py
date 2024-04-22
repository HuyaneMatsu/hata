import vampytest

from ..fields import put_answer_id_into


def _iter_options():
    answer_id = 202404040001
    
    yield 0, False, {'id': None}
    yield 0, True, {'id': None}
    yield answer_id, False, {'id': str(answer_id)}
    yield answer_id, True, {'id': str(answer_id)}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_answer_id_into(answer_id, defaults):
    """
    Tests whether ``put_answer_id_into`` works as intended.
    
    Parameters
    ----------
    answer_id : `int`
        The answer's identifier to serialise.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_answer_id_into(answer_id, {}, defaults)
