from datetime import datetime as DateTime

import vampytest

from ....utils import datetime_to_timestamp

from ..fields import parse_synced_at


def test__parse_synced_at():
    """
    Tests whether ``parse_synced_at`` works as intended.
    """
    synced_at = DateTime(2016, 9, 9)
    
    for input_data, expected_output in (
        ({}, None),
        ({'synced_at': None}, None),
        ({'synced_at': datetime_to_timestamp(synced_at)}, synced_at),
    ):
        output = parse_synced_at(input_data)
        vampytest.assert_eq(output, expected_output)
