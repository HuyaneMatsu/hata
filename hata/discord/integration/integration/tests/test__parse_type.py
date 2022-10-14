import vampytest

from ..integration_type import IntegrationType

from ..fields import parse_type


def test__parse_type():
    """
    Tests whether ``parse_type`` works as intended.
    """
    for input_data, expected_output in (
        ({}, IntegrationType.none),
        ({'type': IntegrationType.none.value}, IntegrationType.none),
        ({'type': IntegrationType.discord.value}, IntegrationType.discord),
    ):
        output = parse_type(input_data)
        vampytest.assert_eq(output, expected_output)
