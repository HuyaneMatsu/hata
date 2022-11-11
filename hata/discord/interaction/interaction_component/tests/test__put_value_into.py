import vampytest

from ..fields import put_value_into


def test__put_value_into():
    """
    Tests whether ``put_value_into`` is working as intended.
    """
    for input_, defaults, expected_output in (
        (None, False, {}),
        (None, True, {'value': None}),
        ('a', False, {'value': 'a'}),
    ):
        data = put_value_into(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
