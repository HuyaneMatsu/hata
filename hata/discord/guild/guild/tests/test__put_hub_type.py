import vampytest

from ..fields import put_hub_type_into
from ..preinstanced import HubType


def test__put_hub_type_into():
    """
    Tests whether ``put_hub_type_into`` works as intended.
    """
    for input_value, defaults, expected_output in (
        (HubType.college, False, {'hub_type': HubType.college.value}),
    ):
        data = put_hub_type_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
