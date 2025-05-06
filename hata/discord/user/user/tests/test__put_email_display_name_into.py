import vampytest

from ..fields import put_display_name


def test__put_display_name():
    """
    Tests whether ``put_display_name`` works as intended.
    """
    for input_, defaults, expected_output in (
        (None, False, {}),
        (None, True, {'global_name': None}),
        ('meow', False, {'global_name': 'meow'}),
    ):
        data = put_display_name(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
