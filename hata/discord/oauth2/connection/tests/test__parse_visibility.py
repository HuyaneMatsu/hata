import vampytest

from ..preinstanced import ConnectionVisibility

from ..fields import parse_visibility


def test__parse_visibility():
    """
    Tests whether ``parse_visibility`` works as intended.
    """
    for input_data, expected_output in (
        ({}, ConnectionVisibility.user_only),
        ({'visibility': ConnectionVisibility.user_only.value}, ConnectionVisibility.user_only),
        ({'visibility': ConnectionVisibility.everyone.value}, ConnectionVisibility.everyone),
    ):
        output = parse_visibility(input_data)
        vampytest.assert_eq(output, expected_output)
