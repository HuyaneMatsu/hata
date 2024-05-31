import vampytest

from ...message.flags import MessageFlag

from ..fields import put_flags_into


def _iter_options():
    yield MessageFlag(0), False, {}
    yield MessageFlag(0), True, {'message': {'flags': 0}}
    yield MessageFlag(1), False, {'message': {'flags': 1}}
    yield MessageFlag(1), True, {'message': {'flags': 1}}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_flags_into(input_value, defaults):
    """
    Tests whether ``put_flags_into`` is working as intended.
    
    Parameters
    ----------
    input_value : ``MessageFlag``
        The value to serialise.
    defaults : `bool`
        Whether fields of their default value should be included in the output.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    return put_flags_into(input_value, {}, defaults)
