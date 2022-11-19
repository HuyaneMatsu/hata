import vampytest

from ..fields import put_rule_id_into


def test__put_rule_id_into():
    """
    Tests whether ``put_rule_id_into`` is working as intended.
    """
    rule_id = 202211160008
    
    for input_, defaults, expected_output in (
        (0, False, {}),
        (0, True, {'rule_id': None}),
        (rule_id, False, {'rule_id': str(rule_id)}),
    ):
        data = put_rule_id_into(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
