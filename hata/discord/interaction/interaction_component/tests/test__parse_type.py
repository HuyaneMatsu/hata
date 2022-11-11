import vampytest

from ....component import ComponentType

from ..fields import parse_type


def test__parse_type():
    """
    Tests whether ``parse_type`` works as intended.
    """
    for input_data, expected_output in (
        ({}, ComponentType.none),
        ({'type': ComponentType.row.value}, ComponentType.row),
    ):
        output = parse_type(input_data)
        vampytest.assert_eq(output, expected_output)
