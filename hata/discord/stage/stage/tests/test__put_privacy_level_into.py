import vampytest

from ....scheduled_event import PrivacyLevel

from ..fields import put_privacy_level_into


def test__put_privacy_level_into():
    """
    Tests whether ``put_privacy_level_into`` works as intended.
    """
    for input_value, defaults, expected_output in (
        (PrivacyLevel.public, False, {'privacy_level': PrivacyLevel.public.value}),
    ):
        data = put_privacy_level_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
