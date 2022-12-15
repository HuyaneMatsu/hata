from datetime import datetime as DateTime

import vampytest

from ....utils import datetime_to_timestamp

from ..fields import parse_application_actioned


def test__parse_application_actioned():
    """
    Tests whether ``parse_application_actioned`` works as intended.
    """
    application_actioned = DateTime(2016, 5, 14)
    
    for input_value, expected_output in (
        ({}, None),
        ({'partner_actioned_timestamp': None}, None),
        ({'partner_actioned_timestamp': datetime_to_timestamp(application_actioned)}, application_actioned),
    ):
        output = parse_application_actioned(input_value)
        vampytest.assert_eq(output, expected_output)
