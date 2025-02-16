import vampytest

from ..fields import put_text_input_style
from ..preinstanced import TextInputStyle


def test__put_text_input_style():
    """
    Tests whether ``put_text_input_style`` is working as intended.
    """
    for input_value, defaults, expected_output in (
        (TextInputStyle.short, False, {'style': TextInputStyle.short.value}),
        (TextInputStyle.paragraph, True, {'style': TextInputStyle.paragraph.value}),
    ):
        data = put_text_input_style(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
