import vampytest

from ..fields import put_raid_protection_into


def test__put_raid_protection_into():
    """
    Tests whether ``put_raid_protection_into`` works as intended.
    """
    for input_, defaults, expected_output in (
        (False, False, {}),
        (False, True, {'mention_raid_protection_enabled': False}),
        (True, False, {'mention_raid_protection_enabled': True}),
    ):
        data = put_raid_protection_into(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
