import vampytest

from ..fields import put_values


def test__put_values():
    """
    Tests whether ``put_values`` is working as intended.
    """
    for input_, defaults, expected_output in (
        (None, False, {}),
        (None, True, {'values': []}),
        (('a', ), False, {'values': ['a']}),
    ):
        data = put_values(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
