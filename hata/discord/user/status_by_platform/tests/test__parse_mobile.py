import vampytest

from ...status_by_platform import Status

from ..fields import parse_mobile


def _iter_options():
    yield (
        {},
        Status.offline,
    )
    
    yield (
        {
            'mobile': Status.online.value,
        },
        Status.online,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_mobile(input_data):
    """
    Tests whether ``parse_mobile`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to test with.
    
    Returns
    -------
    output : ``Status``
    """
    output = parse_mobile(input_data)
    vampytest.assert_instance(output, Status)
    return output
