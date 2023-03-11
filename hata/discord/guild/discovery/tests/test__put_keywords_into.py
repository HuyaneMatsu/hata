import vampytest

from ..fields import put_keywords_into


def test__put_keywords_into():
    """
    Tests whether ``put_keywords_into`` is working as intended.
    """
    for input_value, defaults, expected_output in (
        (None, False, {}),
        (None, True, {'keywords': []}),
        (('a', ), False, {'keywords': ['a']}),
    ):
        data = put_keywords_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
