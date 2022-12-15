import vampytest

from ...discovery_category import DiscoveryCategory

from ..fields import parse_sub_categories


def test__parse_sub_categories():
    """
    Tests whether ``parse_sub_categories`` works as intended.
    """
    for input_data, expected_output in (
        ({}, None),
        ({'category_ids': None}, None),
        ({'category_ids': []}, None),
        ({'category_ids': [DiscoveryCategory.gaming.value]}, (DiscoveryCategory.gaming,)),
    ):
        output = parse_sub_categories(input_data)
        vampytest.assert_eq(output, expected_output)
