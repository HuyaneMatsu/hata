import vampytest

from ..fields import put_parameters_into


def test__put_parameters_into():
    """
    Tests whether ``put_parameters_into`` is working as intended.
    """
    for input_, defaults, expected_output in (
        (None, False, {'parameters': ''}),
        ('', False, {'parameters': ''}),
        ('a', False, {'parameters': 'a'}),
    ):
        data = put_parameters_into(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
