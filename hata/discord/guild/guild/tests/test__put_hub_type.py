import vampytest

from ..fields import put_hub_type
from ..preinstanced import HubType


def test__put_hub_type():
    """
    Tests whether ``put_hub_type`` works as intended.
    """
    for input_value, defaults, expected_output in (
        (HubType.college, False, {'hub_type': HubType.college.value}),
    ):
        data = put_hub_type(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
