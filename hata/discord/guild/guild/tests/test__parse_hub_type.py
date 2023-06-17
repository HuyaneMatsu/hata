import vampytest

from ..fields import parse_hub_type
from ..preinstanced import HubType


def test__parse_hub_type():
    """
    Tests whether ``parse_hub_type`` works as intended.
    """
    for input_data, expected_output in (
        ({}, HubType.none),
        ({'hub_type': HubType.college.value}, HubType.college),
    ):
        output = parse_hub_type(input_data)
        vampytest.assert_eq(output, expected_output)
