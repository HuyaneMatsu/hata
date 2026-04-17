import vampytest

from ...status_by_platform import Status

from ..fields import put_web


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
            'web': Status.offline.value,
        },
    )
    
    yield (
        Status.online,
        False,
        {
            'web': Status.online.value,
        },
    )
    
    yield (
        Status.online,
        True,
        {
            'web': Status.online.value,
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_web(input_value, defaults):
    """
    Tests whether ``put_web`` is working as intended.
    
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
    return put_web(input_value, {}, defaults)
