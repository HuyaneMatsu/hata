import vampytest

from ...status_by_platform import Status

from ..fields import put_status


def _iter_options():
    yield (
        Status.offline,
        False,
        {
            'status': Status.offline.value,
        },
    )
    
    yield (
        Status.offline,
        True,
        {
            'status': Status.offline.value,
        },
    )
    
    yield (
        Status.online,
        False,
        {
            'status': Status.online.value,
        },
    )
    
    yield (
        Status.online,
        True,
        {
            'status': Status.online.value,
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_status(input_value, defaults):
    """
    Tests whether ``put_status`` is working as intended.
    
    Parameters
    ----------
    input_value : ``Status``
        Value to serialize.
    
    defaults : `bool`
        Whether fields as their default value should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_status(input_value, {}, defaults)
