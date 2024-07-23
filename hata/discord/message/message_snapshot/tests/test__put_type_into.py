import vampytest

from ...message.preinstanced import MessageType

from ..fields import put_type_into


def _iter_options():
    yield MessageType.default, False, {}
    yield MessageType.default, True, {'message': {'type': MessageType.default.value}}
    yield MessageType.call, False, {'message': {'type': MessageType.call.value}}
    yield MessageType.call, True, {'message': {'type': MessageType.call.value}}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_type_into(input_value, defaults):
    """
    Tests whether ``put_type_into`` is working as intended.
    
    Parameters
    ----------
    input_value : ``MessageType``
        The value to serialise.
    defaults : `bool`
        Whether fields of their default value should be included in the output.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    return put_type_into(input_value, {}, defaults)
