from datetime import datetime as DateTime

import vampytest

from ....utils import datetime_to_timestamp

from ..fields import put_boosts_since_into


def test__put_boosts_since_into():
    """
    Tests whether ``put_boosts_since_into`` works as intended.
    """
    boosts_since = DateTime(2016, 5, 14)
    
    for input_value, defaults, expected_output in (
        (None, False, {}),
        (None, True, {'premium_since': None}),
        (boosts_since, False, {'premium_since': datetime_to_timestamp(boosts_since)}),
    ):
        output = put_boosts_since_into(input_value, {}, defaults)
        vampytest.assert_eq(output, expected_output)
