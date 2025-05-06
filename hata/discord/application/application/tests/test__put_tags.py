import vampytest

from ..fields import put_tags


def test__put_tags():
    """
    Tests whether ``put_tags`` is working as intended.
    """
    for input_, defaults, expected_output in (
        (None, False, {}),
        (None, True, {'tags': []}),
        (('a', ), False, {'tags': ['a']}),
    ):
        data = put_tags(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
