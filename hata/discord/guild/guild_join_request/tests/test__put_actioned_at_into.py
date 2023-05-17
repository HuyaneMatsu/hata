from datetime import datetime as DateTime

import vampytest

from ....utils import datetime_to_timestamp

from ..fields import put_actioned_at_into


def test__put_actioned_at_into():
    """
    Tests whether ``put_actioned_at_into`` works as intended.
    """
    actioned_at = DateTime(2016, 5, 14)
    
    for input_value, defaults, expected_output in (
        (None, False, {}),
        (None, True, {'actioned_at': None}),
        (actioned_at, False, {'actioned_at': datetime_to_timestamp(actioned_at)}),
    ):
        output = put_actioned_at_into(input_value, {}, defaults)
        vampytest.assert_eq(output, expected_output)
