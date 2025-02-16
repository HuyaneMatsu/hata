import vampytest

from ..fields import put_matched_keyword


def test__put_matched_keyword():
    """
    Tests whether ``put_matched_keyword`` is working as intended.
    """
    for input_, defaults, expected_output in (
        (None, False, {'matched_keyword': ''}),
        ('a', False, {'matched_keyword': 'a'}),
    ):
        data = put_matched_keyword(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
