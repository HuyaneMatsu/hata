from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....user import User

from ..scheduled_event_user_entry import ScheduledEventUserEntry


def test__ScheduledEventUserEntry__repr():
    """
    Tests whether ``ScheduledEventUserEntry.__repr__`` works as intended.
    """
    scheduled_event_id = 202602100041
    timestamp = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    user = User.precreate(
        202602100042,
        name = 'Suwako',
    )
    
    scheduled_event_user_entry = ScheduledEventUserEntry(
        scheduled_event_id = scheduled_event_id,
        timestamp = timestamp,
        user = user,
    )
    
    output = repr(scheduled_event_user_entry)
    vampytest.assert_instance(output, str)


def test__ScheduledEventUserEntry__hash():
    """
    Tests whether ``ScheduledEventUserEntry.__hash__`` works as intended.
    """
    scheduled_event_id = 202602100043
    timestamp = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    user = User.precreate(
        202602100044,
        name = 'Suwako',
    )
    
    scheduled_event_user_entry = ScheduledEventUserEntry(
        scheduled_event_id = scheduled_event_id,
        timestamp = timestamp,
        user = user,
    )
    
    output = hash(scheduled_event_user_entry)
    vampytest.assert_instance(output, int)


def _iter_options__eq():
    
    scheduled_event_id = 202602100045
    timestamp = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    user = User.precreate(
        202602100046,
        name = 'Suwako',
    )
    
    keyword_parameters = {
        'scheduled_event_id': scheduled_event_id,
        'timestamp': timestamp,
        'user': user,
    }
    
    yield (
        keyword_parameters,
        keyword_parameters,
        True,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'scheduled_event_id': 202602100047,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'timestamp': DateTime(2016, 5, 24, tzinfo = TimeZone.utc),
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'user': User.precreate(
                202602100048,
                name = 'Suwako',
            ),
        },
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__ScheduledEventUserEntry__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``ScheduledEventUserEntry.__eq__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters_0 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    keyword_parameters_1 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : `bool`
    """
    scheduled_event_user_entry_0 = ScheduledEventUserEntry(**keyword_parameters_0)
    scheduled_event_user_entry_1 = ScheduledEventUserEntry(**keyword_parameters_1)
    
    output = scheduled_event_user_entry_0 == scheduled_event_user_entry_1
    vampytest.assert_instance(output, bool)
    return output
