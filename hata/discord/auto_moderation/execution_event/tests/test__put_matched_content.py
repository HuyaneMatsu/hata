import vampytest

from ..fields import put_matched_content


def test__put_matched_content():
    """
    Tests whether ``put_matched_content`` is working as intended.
    """
    for input_, defaults, expected_output in (
        (None, False, {'matched_content': ''}),
        ('a', False, {'matched_content': 'a'}),
    ):
        data = put_matched_content(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
