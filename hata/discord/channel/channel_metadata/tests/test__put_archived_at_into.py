from datetime import datetime as DateTime

import vampytest

from ....utils import datetime_to_timestamp

from ..fields import put_archived_at_into


def test__put_archived_at_into():
    """
    Tests whether ``put_archived_at_into`` is working as intended.
    """
    archived_at = DateTime(2016, 9, 9)
    
    for input_value, defaults, expected_output in (
        (None, False, {}),
        (None, True, {'thread_metadata': {'archive_timestamp': None}}),
        (archived_at, False, {'thread_metadata': {'archive_timestamp': datetime_to_timestamp(archived_at)}}),
    ):
        data = put_archived_at_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
