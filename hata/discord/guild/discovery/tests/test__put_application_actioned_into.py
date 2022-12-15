from datetime import datetime as DateTime

import vampytest

from ....utils import datetime_to_timestamp

from ..fields import put_application_actioned_into


def test__put_application_actioned_into():
    """
    Tests whether ``put_application_actioned_into`` works as intended.
    """
    application_actioned = DateTime(2016, 5, 14)
    
    for input_value, defaults, expected_output in (
        (None, False, {}),
        (None, True, {'partner_actioned_timestamp': None}),
        (application_actioned, False, {'partner_actioned_timestamp': datetime_to_timestamp(application_actioned)}),
    ):
        output = put_application_actioned_into(input_value, {}, defaults)
        vampytest.assert_eq(output, expected_output)
