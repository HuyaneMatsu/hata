from datetime import datetime as DateTime

import vampytest

from ....utils import datetime_to_timestamp

from ..fields import put_synced_at_into


def test__put_synced_at_into():
    """
    Tests whether ``put_synced_at_into`` is working as intended.
    """
    synced_at = DateTime(2016, 9, 9)
    
    for input_, defaults, expected_output in (
        (None, False, {}),
        (None, True, {'synced_at': None}),
        (synced_at, False, {'synced_at': datetime_to_timestamp(synced_at)}),
    ):
        data = put_synced_at_into(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
