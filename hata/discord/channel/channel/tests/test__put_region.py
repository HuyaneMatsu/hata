import vampytest

from ..fields import put_region_into
from ..preinstanced import VoiceRegion


def test__put_region_into():
    """
    Tests whether ``put_region_into`` is working as intended.
    """
    for input_, defaults, expected_output in (
        (VoiceRegion.brazil, False, {'rtc_region': VoiceRegion.brazil.value}),
    ):
        data = put_region_into(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
