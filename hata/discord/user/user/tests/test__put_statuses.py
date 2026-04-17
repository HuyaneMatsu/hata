import vampytest

from ...status_by_platform import Status, StatusByPlatform

from ..fields import put_status_by_platform


def _iter_options():
    yield (
        None,
        False,
        {
            'client_status': {},
        },
    )
    
    yield (
        None,
        True,
        {
            'client_status': {},
        },
    )
    
    status_by_platform = StatusByPlatform(
        mobile = Status.online,
    )
    
    yield (
        status_by_platform,
        False,
        {
            'client_status': status_by_platform.to_data(defaults = False),
        },
    )
    
    yield (
        status_by_platform,
        True,
        {
            'client_status': status_by_platform.to_data(defaults = True),
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_status_by_platform(input_value, defaults):
    """
    Tests whether ``put_status_by_platform`` works as intended.
    
    Parameters
    ----------
    input_value : ``None | StatusByPlatform``
        Value to serialize.
    
    defaults : `bool`
        Whether values as their default should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_status_by_platform(input_value, {}, defaults)
