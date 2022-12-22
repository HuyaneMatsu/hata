from datetime import datetime as DateTime

import vampytest

from ....utils import datetime_to_timestamp

from ..fields import put_edited_at_into


def test__put_edited_at_into():
    """
    Tests whether ``put_edited_at_into`` works as intended.
    """
    edited_at = DateTime(2016, 5, 14)
    
    for input_value, defaults, expected_output in (
        (None, False, {}),
        (None, True, {'version': None}),
        (edited_at, False, {'version': datetime_to_timestamp(edited_at)}),
    ):
        output = put_edited_at_into(input_value, {}, defaults)
        vampytest.assert_eq(output, expected_output)
