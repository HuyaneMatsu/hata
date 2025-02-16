import vampytest

from ..fields import put_join


def test__put_join():
    """
    Tests whether ``put_join`` is working as intended.
    """
    for input_value, defaults, expected_output in (
        (None, False, {}),
        ('a', False, {'join': 'a'}),
    ):
        data = put_join(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
