import vampytest

from ...constants import AUTO_ARCHIVE_DEFAULT

from ..default_thread_auto_archive_after import validate_default_thread_auto_archive_after


def test__validate_default_thread_auto_archive_after():
    """
    Tests whether ``validate_default_thread_auto_archive_after`` works as intended.
    """
    for input_parameter, expected_output in (
        (AUTO_ARCHIVE_DEFAULT, AUTO_ARCHIVE_DEFAULT),
    ):
        output = validate_default_thread_auto_archive_after(input_parameter)
        vampytest.assert_eq(output, expected_output)
