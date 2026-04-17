import vampytest

from ...discovery_category import DiscoveryCategory

from ..fields import put_primary_category


def test__put_primary_category():
    """
    Tests whether ``put_primary_category`` is working as intended.
    """
    for input_value, defaults, expected_output in (
        (DiscoveryCategory.gaming, False, {'primary_category_id': DiscoveryCategory.gaming.value}),
    ):
        data = put_primary_category(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
