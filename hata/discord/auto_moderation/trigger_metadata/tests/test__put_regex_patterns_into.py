import vampytest

from ..fields import put_regex_patterns_into


def test__put_regex_patterns_into():
    """
    Tests whether ``put_regex_patterns_into`` is working as intended.
    """
    for input_, defaults, expected_output in (
        (None, False, {}),
        (None, True, {'regex_patterns': []}),
        (('a', ), False, {'regex_patterns': ['a']}),
    ):
        data = put_regex_patterns_into(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
