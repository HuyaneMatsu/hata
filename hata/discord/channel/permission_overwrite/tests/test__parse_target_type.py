import vampytest

from ..fields import parse_target_type
from ..preinstanced import PermissionOverwriteTargetType


def _iter_options():
    yield {}, PermissionOverwriteTargetType.unknown
    yield {'type': None}, PermissionOverwriteTargetType.unknown
    yield {'type': PermissionOverwriteTargetType.user.value}, PermissionOverwriteTargetType.user


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_target_type(input_data):
    """
    Tests whether ``parse_target_type`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse the target type from.
    
    Returns
    -------
    output : ``PermissionOverwriteTargetType``
    """
    output = parse_target_type(input_data)
    vampytest.assert_instance(output, PermissionOverwriteTargetType)
    return output
