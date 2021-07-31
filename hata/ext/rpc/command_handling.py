__all__ = ()

import sys

from ...discord.activity import ActivityRich

from .dispatch_handling import DISPATCH_EVENT_HANDLERS
from .constants import PAYLOAD_KEY_EVENT, PAYLOAD_KEY_DATA, PAYLOAD_KEY_NONCE, PAYLOAD_COMMAND_DISPATCH, \
    PAYLOAD_COMMAND_CERTIFIED_DEVICES_SET, PAYLOAD_COMMAND_ACTIVITY_SET

def handle_command_DISPATCH(self, data):
    dispatch_event_name = data[PAYLOAD_KEY_EVENT]
    try:
        dispatch_event_handler = DISPATCH_EVENT_HANDLERS[dispatch_event_name]
    except KeyError:
        sys.stderr.write(
            f'{self!r} cannot handle dispatch event {dispatch_event_name!r}.\n'
            f'Received data: {data!r}\n'
        )
        return
    
    dispatch_event_handler(self, data[PAYLOAD_KEY_DATA])


def handle_command_CERTIFIED_DEVICES_SET(self, data):
    try:
        nonce = data[PAYLOAD_KEY_NONCE]
    except KeyError:
        pass
    else:
        try:
            waiter = self._response_waiters[nonce]
        except KeyError:
            pass
        else:
            waiter.set_result_if_pending(None)


def handle_command_ACTIVITY_SET(self, data):
    nonce = data.get(PAYLOAD_KEY_NONCE)
    if (nonce is None):
        return
    
    try:
        response_waiter = self._response_waiters[nonce]
    except KeyError:
        return
    
    activity = ActivityRich.from_data(data[PAYLOAD_KEY_DATA])
    response_waiter.set_result_if_pending(activity)


COMMAND_HANDLERS = {
    PAYLOAD_COMMAND_DISPATCH: handle_command_DISPATCH,
    PAYLOAD_COMMAND_CERTIFIED_DEVICES_SET: handle_command_CERTIFIED_DEVICES_SET,
    PAYLOAD_COMMAND_ACTIVITY_SET: handle_command_ACTIVITY_SET,
}

del handle_command_DISPATCH
del handle_command_CERTIFIED_DEVICES_SET
del handle_command_ACTIVITY_SET

