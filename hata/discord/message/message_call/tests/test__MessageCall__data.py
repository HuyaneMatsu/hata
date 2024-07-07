from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....utils import datetime_to_timestamp

from ..message_call import MessageCall

from .test__MessageCall__constructor import _assert_fields_set


def test__MessageCall__from_data():
    """
    Tests whether ``MessageCall.from_data`` works as intended.
    """
    ended_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    user_ids = [202304280002, 202304280003]
    
    data = {
        'ended_timestamp': datetime_to_timestamp(ended_at),
        'participants': [str(user_id) for user_id in user_ids],
    }
    
    message_call = MessageCall.from_data(data)
    _assert_fields_set(message_call)

    vampytest.assert_eq(message_call.ended_at, ended_at)
    vampytest.assert_eq(message_call.user_ids, tuple(user_ids))


def test__MessageCall__to_data():
    """
    Tests whether ``MessageCall.to_data`` works as intended.
    
    Case: include defaults.
    """
    ended_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    user_ids = [202304280004, 202304280005]
    
    message_call = MessageCall(
        ended_at = ended_at,
        user_ids = user_ids,
    )
    
    vampytest.assert_eq(
        message_call.to_data(
            defaults = True,
        ),
        {
            'ended_timestamp': datetime_to_timestamp(ended_at),
            'participants':[str(user_id) for user_id in user_ids],
        },
    )
