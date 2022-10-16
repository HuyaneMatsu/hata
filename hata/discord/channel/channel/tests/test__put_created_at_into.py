from datetime import datetime as DateTime

import vampytest

from ....utils import datetime_to_timestamp

from ..fields import put_created_at_into


def test__put_created_at_into():
    """
    Tests whether ``put_created_at_into`` is working as intended.
    """
    created_at = DateTime(2016, 9, 9)
    
    for input_, defaults, expected_output in (
        (None, False, {}),
        (None, True, {'thread_metadata': {'create_timestamp': None}}),
        (created_at, False, {'thread_metadata': {'create_timestamp': datetime_to_timestamp(created_at)}}),
    ):
        data = put_created_at_into(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
