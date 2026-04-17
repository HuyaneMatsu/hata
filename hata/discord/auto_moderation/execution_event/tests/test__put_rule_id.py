import vampytest

from ..fields import put_rule_id


def test__put_rule_id():
    """
    Tests whether ``put_rule_id`` is working as intended.
    """
    rule_id = 202211160008
    
    for input_, defaults, expected_output in (
        (0, False, {}),
        (0, True, {'rule_id': None}),
        (rule_id, False, {'rule_id': str(rule_id)}),
    ):
        data = put_rule_id(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
