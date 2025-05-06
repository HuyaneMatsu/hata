import vampytest

from ..fields import put_parameters


def test__put_parameters():
    """
    Tests whether ``put_parameters`` is working as intended.
    """
    for input_, defaults, expected_output in (
        (None, False, {'parameters': ''}),
        ('', False, {'parameters': ''}),
        ('a', False, {'parameters': 'a'}),
    ):
        data = put_parameters(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
