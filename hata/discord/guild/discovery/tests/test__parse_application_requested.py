from datetime import datetime as DateTime

import vampytest

from ....utils import datetime_to_timestamp

from ..fields import parse_application_requested


def test__parse_application_requested():
    """
    Tests whether ``parse_application_requested`` works as intended.
    """
    application_requested = DateTime(2016, 5, 14)
    
    for input_value, expected_output in (
        ({}, None),
        ({'partner_application_timestamp': None}, None),
        ({'partner_application_timestamp': datetime_to_timestamp(application_requested)}, application_requested),
    ):
        output = parse_application_requested(input_value)
        vampytest.assert_eq(output, expected_output)
