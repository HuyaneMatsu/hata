import vampytest

from ....permission import Permission

from ..fields import put_permissions


def test__put_permissions():
    """
    Tests whether ``put_permissions`` is working as intended.
    """
    for input_value, defaults, expected_output in (
        (Permission(0), False, {'permissions': '0'}),
        (Permission(0), True, {'permissions': '0'}),
        (Permission(1), False, {'permissions': '1'}),
    ):
        data = put_permissions(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
