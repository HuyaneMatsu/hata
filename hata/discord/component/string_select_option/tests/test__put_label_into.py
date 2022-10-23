import vampytest

from ..fields import put_label_into


def test__put_label_into():
    """
    Tests whether ``put_label_into`` is working as intended.
    """
    for input_, defaults, expected_output in (
        ('', False, {'label': ''}),
        ('a', False, {'label': 'a'}),
    ):
        data = put_label_into(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
