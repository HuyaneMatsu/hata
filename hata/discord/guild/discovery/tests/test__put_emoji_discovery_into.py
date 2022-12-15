import vampytest

from ..fields import put_emoji_discovery_into


def test__put_emoji_discovery_into():
    """
    Tests whether ``put_emoji_discovery_into`` works as intended.
    """
    for input_, defaults, expected_output in (
        (False, False, {}),
        (False, True, {'emoji_discoverability_enabled': False}),
        (True, False, {'emoji_discoverability_enabled': True}),
    ):
        data = put_emoji_discovery_into(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
