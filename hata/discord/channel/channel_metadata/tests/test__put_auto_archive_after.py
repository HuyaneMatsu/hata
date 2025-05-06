import vampytest

from ..constants import AUTO_ARCHIVE_DEFAULT
from ..fields import put_auto_archive_after


def test__put_auto_archive_after():
    """
    Tests whether ``put_auto_archive_after`` is working as intended.
    """
    for input_value, defaults, expected_output in (
        (AUTO_ARCHIVE_DEFAULT, False, {}),
        (AUTO_ARCHIVE_DEFAULT, True, {'thread_metadata': {'auto_archive_duration': AUTO_ARCHIVE_DEFAULT // 60}}),
        (60, False, {'thread_metadata': {'auto_archive_duration': 1}}),
    ):
        data = put_auto_archive_after(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
