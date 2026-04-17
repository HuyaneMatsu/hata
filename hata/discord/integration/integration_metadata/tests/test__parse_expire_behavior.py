import vampytest

from ..preinstanced import IntegrationExpireBehavior

from ..fields import parse_expire_behavior


def test__parse_expire_behavior():
    """
    Tests whether ``parse_expire_behavior`` works as intended.
    """
    for input_data, expected_output in (
        ({}, IntegrationExpireBehavior.remove_role),
        ({'expire_behavior': IntegrationExpireBehavior.remove_role.value}, IntegrationExpireBehavior.remove_role),
        ({'expire_behavior': IntegrationExpireBehavior.kick.value}, IntegrationExpireBehavior.kick),
    ):
        output = parse_expire_behavior(input_data)
        vampytest.assert_eq(output, expected_output)
