from datetime import datetime as DateTime

import vampytest

from ....utils import datetime_to_timestamp

from ..fields import parse_actioned_at


def test__parse_actioned_at():
    """
    Tests whether ``parse_actioned_at`` works as intended.
    """
    actioned_at = DateTime(2016, 5, 14)
    
    for input_value, expected_output in (
        ({}, None),
        ({'actioned_at': None}, None),
        ({'actioned_at': datetime_to_timestamp(actioned_at)}, actioned_at),
    ):
        output = parse_actioned_at(input_value)
        vampytest.assert_eq(output, expected_output)
