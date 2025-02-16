import vampytest

from ..fields import put_placeholder


def test__put_placeholder():
    """
    Tests whether ``put_placeholder`` is working as intended.
    """
    for input_value, defaults, expected_output in (
        (None, False, {}),
        ('a', False, {'placeholder': 'a'}),
    ):
        data = put_placeholder(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
