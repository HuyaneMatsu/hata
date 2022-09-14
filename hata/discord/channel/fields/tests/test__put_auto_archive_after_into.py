import vampytest

from ...constants import AUTO_ARCHIVE_DEFAULT

from ..auto_archive_after import put_auto_archive_after_into


def test__put_auto_archive_after_into():
    """
    Tests whether ``put_auto_archive_after_into`` is working as intended.
    """
    for input_, defaults, expected_output in (
        (AUTO_ARCHIVE_DEFAULT, False, {}),
        (AUTO_ARCHIVE_DEFAULT, True, {'thread_metadata': {'auto_archive_duration': AUTO_ARCHIVE_DEFAULT // 60}}),
        (60, False, {'thread_metadata': {'auto_archive_duration': 1}}),
    ):
        data = put_auto_archive_after_into(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
