import vampytest

from ..fields import put_target_type_into
from ..preinstanced import ApplicationCommandPermissionOverwriteTargetType


def _iter_options():
    yield (
        ApplicationCommandPermissionOverwriteTargetType.role,
        False,
        {'type': ApplicationCommandPermissionOverwriteTargetType.role.value},
    )
    
    yield (
        ApplicationCommandPermissionOverwriteTargetType.role,
        True,
        {'type': ApplicationCommandPermissionOverwriteTargetType.role.value},
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_target_type_into(input_value, defaults):
    """
    Tests whether ``put_target_type_into`` works as intended.
    
    Parameters
    ----------
    input_value : ``ApplicationCommandPermissionOverwriteTargetType``
        The value to serialise.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_target_type_into(input_value, {}, defaults)
