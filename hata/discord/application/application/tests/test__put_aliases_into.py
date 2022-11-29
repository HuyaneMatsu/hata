import vampytest

from ..fields import put_aliases_into


def test__put_aliases_into():
    """
    Tests whether ``put_aliases_into`` is working as intended.
    """
    for input_, defaults, expected_output in (
        (None, False, {}),
        (None, True, {'aliases': []}),
        (('a', ), False, {'aliases': ['a']}),
    ):
        data = put_aliases_into(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
