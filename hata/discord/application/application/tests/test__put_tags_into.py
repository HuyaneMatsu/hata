import vampytest

from ..fields import put_tags_into


def test__put_tags_into():
    """
    Tests whether ``put_tags_into`` is working as intended.
    """
    for input_, defaults, expected_output in (
        (None, False, {}),
        (None, True, {'tags': []}),
        (('a', ), False, {'tags': ['a']}),
    ):
        data = put_tags_into(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
