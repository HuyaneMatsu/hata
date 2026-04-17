import vampytest

from ...status_by_platform import Status

from ..fields import put_desktop


def _iter_options():
    yield (
        Status.offline,
        False,
        {},
    )
    
    yield (
        Status.offline,
        True,
        {
            'desktop': Status.offline.value,
        },
    )
    
    yield (
        Status.online,
        False,
        {
            'desktop': Status.online.value,
        },
    )
    
    yield (
        Status.online,
        True,
        {
            'desktop': Status.online.value,
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_desktop(input_value, defaults):
    """
    Tests whether ``put_desktop`` is working as intended.
    
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
    return put_desktop(input_value, {}, defaults)
