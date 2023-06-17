import vampytest

from ..fields import parse_content_filter
from ..preinstanced import ContentFilterLevel


def test__parse_content_filter():
    """
    Tests whether ``parse_content_filter`` works as intended.
    """
    for input_data, expected_output in (
        ({}, ContentFilterLevel.disabled),
        ({'explicit_content_filter': ContentFilterLevel.no_role.value}, ContentFilterLevel.no_role),
    ):
        output = parse_content_filter(input_data)
        vampytest.assert_eq(output, expected_output)
