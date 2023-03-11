import vampytest

from ...discovery_category import DiscoveryCategory

from ..fields import put_sub_categories_into


def test__put_sub_categories_into():
    """
    Tests whether ``put_sub_categories_into`` is working as intended.
    """
    for input_value, defaults, expected_output in (
        (None, False, {'category_ids': []}),
        ((DiscoveryCategory.gaming, ), True, {'category_ids': [DiscoveryCategory.gaming.value]}),
    ):
        data = put_sub_categories_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
