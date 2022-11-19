import vampytest

from ..fields import put_excluded_keywords_into


def test__put_excluded_keywords_into():
    """
    Tests whether ``put_excluded_keywords_into`` is working as intended.
    """
    for input_, defaults, expected_output in (
        (None, False, {}),
        (None, True, {'allow_list': []}),
        (('a', ), False, {'allow_list': ['a']}),
    ):
        data = put_excluded_keywords_into(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
