from datetime import datetime as DateTime

import vampytest

from ....utils import datetime_to_timestamp

from ..archived_at import parse_archived_at


def test__parse_archived_at():
    """
    Tests whether ``parse_archived_at`` works as intended.
    """
    archived_at = DateTime(2016, 9, 9)
    
    for input_data, expected_output in (
        ({}, None),
        ({'thread_metadata': {}}, None),
        ({'thread_metadata': {'archive_timestamp': None}}, None),
        ({'thread_metadata': {'archive_timestamp': datetime_to_timestamp(archived_at)}}, archived_at),
    ):
        output = parse_archived_at(input_data)
        vampytest.assert_eq(output, expected_output)
