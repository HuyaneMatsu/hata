import vampytest

from ....component import ComponentType

from ..fields import put_type_into


def test__put_type_into():
    """
    Tests whether ``put_type_into`` is working as intended.
    """
    for input_value, defaults, expected_output in (
        (ComponentType.row, True, {'type': ComponentType.row.value}),
    ):
        data = put_type_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
