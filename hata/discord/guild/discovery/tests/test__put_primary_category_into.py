import vampytest

from ...discovery_category import DiscoveryCategory

from ..fields import put_primary_category_into


def test__put_primary_category_into():
    """
    Tests whether ``put_primary_category_into`` is working as intended.
    """
    for input_, defaults, expected_output in (
        (DiscoveryCategory.gaming, False, {'primary_category_id': DiscoveryCategory.gaming.value}),
    ):
        data = put_primary_category_into(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
