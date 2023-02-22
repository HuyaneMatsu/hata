import vampytest

from ..fields import put_id_into


def test__put_id_into():
    """
    Tests whether ``put_id_into`` is working as intended.
    """
    rule_id = 202211170029
    
    for input_value, defaults, expected_output in (
        (rule_id, False, {'id': str(rule_id)}),
    ):
        data = put_id_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
