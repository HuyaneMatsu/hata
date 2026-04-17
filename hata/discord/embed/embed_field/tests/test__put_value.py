import vampytest

from ..fields import put_value


def test__put_value():
    """
    Tests whether ``put_value`` is working as intended.
    """
    for input_, defaults, expected_output in (
        (None, False, {'value': ''}),
        ('', False, {'value': ''}),
        ('a', False, {'value': 'a'}),
    ):
        data = put_value(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
