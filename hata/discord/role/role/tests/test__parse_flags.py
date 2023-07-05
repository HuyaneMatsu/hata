import vampytest

from ..fields import parse_flags
from ..flags import RoleFlag


def _iter_options():
    yield {}, RoleFlag(0)
    yield {'flags': 1}, RoleFlag(1)


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
    output : ``RoleFlag``
    """
    output = parse_flags(input_data)
    vampytest.assert_instance(output, RoleFlag)
    return output
