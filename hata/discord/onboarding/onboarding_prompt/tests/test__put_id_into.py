import vampytest

from ..fields import put_id_into


def test__put_id_into():
    """
    Tests whether ``put_id_into`` works as intended.
    """
    prompt_id = 202303040001
    
    for input_value, defaults, expected_output in (
        (prompt_id, False, {'id': str(prompt_id)}),
    ):
        data = put_id_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
