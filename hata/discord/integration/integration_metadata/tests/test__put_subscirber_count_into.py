import vampytest

from ..constants import SUBSCRIBER_COUNT_DEFAULT
from ..fields import put_subscriber_count


def test__put_default_auto_archive_after_into():
    """
    Tests whether ``put_subscriber_count`` is working as intended.
    """
    for input_, defaults, expected_output in (
        (SUBSCRIBER_COUNT_DEFAULT, False, {}),
        (SUBSCRIBER_COUNT_DEFAULT, True, {'subscriber_count': SUBSCRIBER_COUNT_DEFAULT}),
        (1, False, {'subscriber_count': 1}),
    ):
        data = put_subscriber_count(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
