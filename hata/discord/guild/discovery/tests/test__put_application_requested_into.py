from datetime import datetime as DateTime

import vampytest

from ....utils import datetime_to_timestamp

from ..fields import put_application_requested_into


def test__put_application_requested_into():
    """
    Tests whether ``put_application_requested_into`` works as intended.
    """
    application_requested = DateTime(2016, 5, 14)
    
    for input_value, defaults, expected_output in (
        (None, False, {}),
        (None, True, {'partner_application_timestamp': None}),
        (application_requested, False, {'partner_application_timestamp': datetime_to_timestamp(application_requested)}),
    ):
        output = put_application_requested_into(input_value, {}, defaults)
        vampytest.assert_eq(output, expected_output)
