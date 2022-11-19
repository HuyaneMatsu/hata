import vampytest

from ..fields import put_matched_keyword_into


def test__put_matched_keyword_into():
    """
    Tests whether ``put_matched_keyword_into`` is working as intended.
    """
    for input_, defaults, expected_output in (
        (None, False, {'matched_keyword': ''}),
        ('a', False, {'matched_keyword': 'a'}),
    ):
        data = put_matched_keyword_into(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
