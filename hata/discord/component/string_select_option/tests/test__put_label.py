import vampytest

from ..fields import put_label


def test__put_label():
    """
    Tests whether ``put_label`` is working as intended.
    """
    for input_, defaults, expected_output in (
        ('', False, {'label': ''}),
        ('a', False, {'label': 'a'}),
    ):
        data = put_label(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
