import vampytest

from ....component import ComponentType

from ..fields import parse_component_type


def test__parse_component_type():
    """
    Tests whether ``parse_component_type`` works as intended.
    """
    for input_data, expected_output in (
        ({}, ComponentType.none),
        ({'component_type': ComponentType.button.value}, ComponentType.button),
    ):
        output = parse_component_type(input_data)
        vampytest.assert_eq(output, expected_output)
