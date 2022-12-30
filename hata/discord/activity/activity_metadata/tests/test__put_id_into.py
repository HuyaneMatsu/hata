import vampytest

from ..fields import put_id_into


def test__put_id_into():
    """
    Tests whether ``put_id_into`` works as intended.
    """
    activity_id = 202212300002
    
    for input_value, defaults, expected_output in (
        (0, False, {}),
        (0, True, {}),
        (activity_id, False, {'id': format(activity_id, 'x')}),
    ):
        data = put_id_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
