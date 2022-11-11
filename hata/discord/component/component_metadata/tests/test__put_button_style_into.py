import vampytest

from ..fields import put_button_style_into
from ..preinstanced import ButtonStyle


def test__put_button_style_into():
    """
    Tests whether ``put_button_style_into`` is working as intended.
    """
    for input_, defaults, expected_output in (
        (ButtonStyle.red, False, {'style': ButtonStyle.red.value}),
        (ButtonStyle.blue, True, {'style': ButtonStyle.blue.value}),
    ):
        data = put_button_style_into(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
