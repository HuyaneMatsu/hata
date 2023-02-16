import vampytest

from ..preinstanced import ConnectionVisibility

from ..fields import parse_metadata_visibility


def test__parse_metadata_visibility():
    """
    Tests whether ``parse_metadata_visibility`` works as intended.
    """
    for input_data, expected_output in (
        ({}, ConnectionVisibility.user_only),
        ({'metadata_visibility': ConnectionVisibility.user_only.value}, ConnectionVisibility.user_only),
        ({'metadata_visibility': ConnectionVisibility.everyone.value}, ConnectionVisibility.everyone),
    ):
        output = parse_metadata_visibility(input_data)
        vampytest.assert_eq(output, expected_output)
