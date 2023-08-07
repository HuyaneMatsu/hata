import vampytest

from ...preinstanced import PermissionOverwriteTargetType

from ..target_type import put_target_type_into


def _iter_options():
    yield PermissionOverwriteTargetType.user, False, {'type': PermissionOverwriteTargetType.user.value}
    yield PermissionOverwriteTargetType.user, True, {'type': PermissionOverwriteTargetType.user.value}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_target_type_into(input_value, defaults):
    """
    Tests whether ``put_target_type_into`` works as intended.
    
    Parameters
    ----------
    input_value : ``PermissionOverwriteTargetType``
        The value to serialise.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_target_type_into(input_value, {}, defaults)
