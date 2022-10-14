import vampytest

from ..fields import put_two_way_link_into


def test__put_two_way_link_into():
    """
    Tests whether ``put_two_way_link_into`` is working as intended.
    """
    for input_, defaults, expected_output in (
        (False, False, {}),
        (False, True, {'two_way_link': False}),
        (True, False, {'two_way_link': True}),
    ):
        data = put_two_way_link_into(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
