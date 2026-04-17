import vampytest

from ..fields import put_distributor


def test__put_distributor():
    """
    Tests whether ``put_distributor`` works as intended.
    """
    for input_, defaults, expected_output in (
        ('', False, {'distributor': ''}),
        ('a', False, {'distributor': 'a'}),
    ):
        data = put_distributor(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
