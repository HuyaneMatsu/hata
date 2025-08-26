import vampytest

from ...status_by_platform import Status

from ..fields import parse_status


def _iter_options():
    yield (
        {},
        Status.offline,
    )
    
    yield (
        {
            'status': Status.online.value,
        },
        Status.online,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_status(input_data):
    """
    Tests whether ``parse_status`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to test with.
    
    Returns
    -------
    output : ``Status``
    """
    output = parse_status(input_data)
    vampytest.assert_instance(output, Status)
    return output
