import vampytest

from ..fields import put_premium_type
from ..preinstanced import PremiumType


def test__put_premium_type():
    """
    Tests whether ``put_premium_type`` is working as intended.
    """
    for input_value, defaults, expected_output in (
        (PremiumType.nitro, False, {'premium_type': PremiumType.nitro.value}),
    ):
        data = put_premium_type(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
