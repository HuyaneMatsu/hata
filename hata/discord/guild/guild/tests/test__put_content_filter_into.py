import vampytest

from ..fields import put_content_filter_into
from ..preinstanced import ContentFilterLevel


def test__put_content_filter_into():
    """
    Tests whether ``put_content_filter_into`` works as intended.
    """
    for input_value, defaults, expected_output in (
        (ContentFilterLevel.no_role, False, {'explicit_content_filter': ContentFilterLevel.no_role.value}),
    ):
        data = put_content_filter_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
