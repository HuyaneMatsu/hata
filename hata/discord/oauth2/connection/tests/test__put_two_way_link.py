import vampytest

from ..fields import put_two_way_link


def test__put_two_way_link():
    """
    Tests whether ``put_two_way_link`` is working as intended.
    """
    for input_value, defaults, expected_output in (
        (False, False, {}),
        (False, True, {'two_way_link': False}),
        (True, False, {'two_way_link': True}),
    ):
        data = put_two_way_link(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
