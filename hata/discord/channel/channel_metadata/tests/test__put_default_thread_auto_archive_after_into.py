import vampytest

from ..constants import AUTO_ARCHIVE_DEFAULT
from ..fields import put_default_thread_auto_archive_after_into


def test__put_default_auto_archive_after_into():
    """
    Tests whether ``put_default_thread_auto_archive_after_into`` is working as intended.
    """
    for input_, defaults, expected_output in (
        (AUTO_ARCHIVE_DEFAULT, False, {}),
        (AUTO_ARCHIVE_DEFAULT, True, {'default_auto_archive_duration': AUTO_ARCHIVE_DEFAULT // 60}),
        (60, False, {'default_auto_archive_duration': 1}),
    ):
        data = put_default_thread_auto_archive_after_into(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
