import vampytest

from ...discovery_category import DiscoveryCategory

from ..fields import parse_primary_category


def test__parse_primary_category():
    """
    Tests whether ``parse_primary_category`` works as intended.
    """
    for input_data, expected_output in (
        ({}, DiscoveryCategory.general),
        ({'primary_category_id': None}, DiscoveryCategory.general),
        ({'primary_category_id': DiscoveryCategory.gaming.value}, DiscoveryCategory.gaming),
    ):
        output = parse_primary_category(input_data)
        vampytest.assert_is(output, expected_output)
