import vampytest

from ..fields import parse_flags
from ..flags import UserFlag


def _iter_options():
    yield {}, UserFlag(0)
    yield {'public_flags': 1}, UserFlag(1)
    yield {'flags': 2}, UserFlag(2)
    yield {'public_flags': 1}, UserFlag(1)
    yield {'flags': 3, 'public_flags': 1}, UserFlag(3)


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_flags(input_data):
    """
    Tests whether ``parse_flags`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse the flags from.
    
    Returns
    -------
    output : ``UserFlag``
    """
    output = parse_flags(input_data)
    vampytest.assert_instance(output, UserFlag)
    return output
