import vampytest

from ..fields import put_aliases


def test__put_aliases():
    """
    Tests whether ``put_aliases`` is working as intended.
    """
    for input_, defaults, expected_output in (
        (None, False, {}),
        (None, True, {'aliases': []}),
        (('a', ), False, {'aliases': ['a']}),
    ):
        data = put_aliases(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
