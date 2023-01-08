import vampytest

from ..fields import put_id_into


def test__put_id_into():
    """
    Tests whether ``put_id_into`` works as intended.
    """
    eula_id = 202211260001
    
    for input_value, defaults, expected_output in (
        (eula_id, False, {'id': str(eula_id)}),
    ):
        data = put_id_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
