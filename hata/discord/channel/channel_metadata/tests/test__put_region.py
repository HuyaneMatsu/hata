import vampytest

from ..fields import put_region
from ..preinstanced import VoiceRegion


def test__put_region():
    """
    Tests whether ``put_region`` is working as intended.
    """
    for input_, defaults, expected_output in (
        (VoiceRegion.brazil, False, {'rtc_region': VoiceRegion.brazil.value}),
    ):
        data = put_region(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
