import vampytest

from ..fields import parse_premium_type
from ..preinstanced import PremiumType


def test__parse_premium_type():
    """
    Tests whether ``parse_premium_type`` works as intended.
    """
    for input_data, expected_output in (
        ({}, PremiumType.none),
        ({'premium_type': PremiumType.none.value}, PremiumType.none),
        ({'premium_type': PremiumType.nitro.value}, PremiumType.nitro),
    ):
        output = parse_premium_type(input_data)
        vampytest.assert_eq(output, expected_output)
