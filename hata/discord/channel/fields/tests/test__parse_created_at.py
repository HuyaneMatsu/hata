from datetime import datetime as DateTime

import vampytest

from ....utils import datetime_to_timestamp

from ..created_at import parse_created_at


def test__parse_created_at():
    """
    Tests whether ``parse_created_at`` works as intended.
    """
    created_at = DateTime(2016, 9, 9)
    
    for input_data, expected_output in (
        ({}, None),
        ({'thread_metadata': {}}, None),
        ({'thread_metadata': {'create_timestamp': None}}, None),
        ({'thread_metadata': {'create_timestamp': datetime_to_timestamp(created_at)}}, created_at),
    ):
        output = parse_created_at(input_data)
        vampytest.assert_eq(output, expected_output)
