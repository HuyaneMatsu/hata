import vampytest

from ..fields import put_title_into


def test__put_title_into():
    """
    Tests whether ``put_title_into`` is working as intended.
    """
    for input_, defaults, expected_output in (
        ('', False, {'label': ''}),
        ('a', False, {'label': 'a'}),
    ):
        data = put_title_into(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
