import vampytest

from ...status_by_platform import Status

from ..fields import put_mobile


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
            'mobile': Status.offline.value,
        },
    )
    
    yield (
        Status.online,
        False,
        {
            'mobile': Status.online.value,
        },
    )
    
    yield (
        Status.online,
        True,
        {
            'mobile': Status.online.value,
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_mobile(input_value, defaults):
    """
    Tests whether ``put_mobile`` is working as intended.
    
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
    return put_mobile(input_value, {}, defaults)
