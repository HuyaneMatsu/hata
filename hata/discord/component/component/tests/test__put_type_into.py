import vampytest

from ..fields import put_type_into
from ..preinstanced import ComponentType


def test__put_type_into():
    """
    Tests whether ``put_type_into`` is working as intended.
    """
    for input_value, defaults, expected_output in (
        (ComponentType.button, False, {'type': ComponentType.button.value}),
    ):
        data = put_type_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
