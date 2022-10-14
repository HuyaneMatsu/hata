import vampytest

from ..integration_application import IntegrationApplication


def test__IntegrationApplication__partial():
    """
    Tests whether ``IntegrationApplication.partial`` works as intended.
    """
    for integration_application, expected_value in (
        (IntegrationApplication.precreate(202210080012), False),
        (IntegrationApplication(), True),
    ):
        vampytest.assert_eq(integration_application.partial, expected_value)
