import vampytest

from ...reaction import ReactionType

from ..fields import put_type


def _iter_options():
    yield ReactionType.standard, False, {'burst': False}
    yield ReactionType.standard, True, {'burst': False}
    yield ReactionType.burst, False, {'burst': True}
    yield ReactionType.burst, True, {'burst': True}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_type(input_value, defaults):
    """
    Tests whether ``put_type`` is working as intended.
    
    Parameters
    ----------
    input_value : ``ReactionType``
        Input value.
    defaults : `bool`
        Whether fields with their default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    return put_type(input_value, {}, defaults)
