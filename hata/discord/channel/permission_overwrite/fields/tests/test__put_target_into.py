import vampytest

from ...preinstanced import PermissionOverwriteTargetType

from ..target import put_target_into


def test__put_target_into():
    """
    Tests whether ``put_target_into`` works as intended.
    """
    target_id = 202210050003
    
    for input_value, expected_data_state, include_internals in (
        (
            (target_id, PermissionOverwriteTargetType.unknown),
            {},
            False,
        ), (
            (target_id, PermissionOverwriteTargetType.unknown),
            {'id': str(target_id)},
            True,
        ), (
            (target_id, PermissionOverwriteTargetType.user),
            {'type': PermissionOverwriteTargetType.user.value},
            False,
        ), (
            (target_id, PermissionOverwriteTargetType.user),
            {'id': str(target_id), 'type': PermissionOverwriteTargetType.user.value},
            True,
        ),
    ):
        data = put_target_into(input_value, {}, True, include_internals = include_internals)
        vampytest.assert_eq(data, expected_data_state)
