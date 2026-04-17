import vampytest

from ..fields import put_target
from ..preinstanced import PermissionOverwriteTargetType


def _iter_options():
    target_id = 202210050003
    
    yield (
        (target_id, PermissionOverwriteTargetType.unknown),
        False,
        False,
        {},
    )
    
    yield (
        (target_id, PermissionOverwriteTargetType.unknown),
        True,
        False,
        {},
    )
    
    yield (
        (target_id, PermissionOverwriteTargetType.unknown),
        False,
        True,
        {'id': str(target_id)},
    )
    
    yield (
        (target_id, PermissionOverwriteTargetType.unknown),
        True,
        True,
        {'id': str(target_id)},
    )
    
    yield (
        (target_id, PermissionOverwriteTargetType.user),
        False,
        False,
        {'type': PermissionOverwriteTargetType.user.value},
    )
    
    yield (
        (target_id, PermissionOverwriteTargetType.user),
        True,
        False,
        {'type': PermissionOverwriteTargetType.user.value},
    )
    
    yield (
        (target_id, PermissionOverwriteTargetType.user),
        False,
        True,
        {'id': str(target_id), 'type': PermissionOverwriteTargetType.user.value},
    )
    
    yield (
        (target_id, PermissionOverwriteTargetType.user),
        True,
        True,
        {'id': str(target_id), 'type': PermissionOverwriteTargetType.user.value},
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_target(input_value, defaults, include_internals):
    """
    Tests whether ``put_target`` works as intended.
    
    Parameters
    ----------
    input_value : `(int, PermissionOverwriteTargetType)`
        The value to serialise.
    defaults : `bool`
        Whether values with their default value should be included in the output as well.
    include_internals : `bool`
        Whether internal fields should be included as well
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_target(input_value, {}, defaults, include_internals = include_internals)
