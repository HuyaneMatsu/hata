import vampytest

from ..fields import put_distributor_into


def test__put_distributor_into():
    """
    Tests whether ``put_distributor_into`` works as intended.
    """
    for input_, defaults, expected_output in (
        ('', False, {'distributor': ''}),
        ('a', False, {'distributor': 'a'}),
    ):
        data = put_distributor_into(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
