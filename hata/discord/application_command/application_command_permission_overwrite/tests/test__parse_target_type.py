import vampytest

from ..fields import parse_target_type
from ..preinstanced import ApplicationCommandPermissionOverwriteTargetType


def _iter_options():
    yield (
        {},
        ApplicationCommandPermissionOverwriteTargetType.none,
    )
    
    yield (
        {'type': None},
        ApplicationCommandPermissionOverwriteTargetType.none,
    )
    
    yield (
        {'type': ApplicationCommandPermissionOverwriteTargetType.role.value},
        ApplicationCommandPermissionOverwriteTargetType.role,
    )


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
    output : ``ApplicationCommandPermissionOverwriteTargetType``
    """
    output = parse_target_type(input_data)
    vampytest.assert_instance(output, ApplicationCommandPermissionOverwriteTargetType)
    return output
