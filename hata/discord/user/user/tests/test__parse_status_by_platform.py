import vampytest

from ...status_by_platform import Status, StatusByPlatform

from ..fields import parse_status_by_platform


def _iter_options():
    yield (
        {},
        None,
    )
    
    yield (
        {
            'client_status': None,
        },
        None,
    )
    
    yield (
        {
            'client_status': {},
        },
        None,
    )
    
    status_by_platform = StatusByPlatform(
        mobile = Status.online,
    )
    
    yield (
        {
            'client_status': status_by_platform.to_data(defaults = False),
        },
        status_by_platform,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_status_by_platform(input_data):
    """
    Tests whether ``parse_status_by_platform` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : ``None | StatusByPlatform``
    """
    output = parse_status_by_platform(input_data)
    vampytest.assert_instance(output, StatusByPlatform, nullable = True)
    return output
