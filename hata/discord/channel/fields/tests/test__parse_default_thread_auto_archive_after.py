import vampytest

from ...constants import AUTO_ARCHIVE_DEFAULT

from ..default_thread_auto_archive_after import parse_default_thread_auto_archive_after


def test__parse_default_thread_auto_archive_after():
    """
    Tests whether ``parse_default_thread_auto_archive_after`` works as intended.
    """
    for input_data, expected_output in (
        ({}, AUTO_ARCHIVE_DEFAULT),
        ({'default_auto_archive_duration': None}, AUTO_ARCHIVE_DEFAULT),
        ({'default_auto_archive_duration': 1}, 60),
    ):
        output = parse_default_thread_auto_archive_after(input_data)
        vampytest.assert_eq(output, expected_output)
