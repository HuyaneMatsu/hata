__all__ = ()

import sys

from .dispatch_handling import DISPATCH_EVENT_HANDLERS
from .constants import PAYLOAD_KEY_EVENT, PAYLOAD_KEY_DATA, PAYLOAD_KEY_NONCE, PAYLOAD_COMMAND_DISPATCH, \
    PAYLOAD_COMMAND_CERTIFIED_DEVICES_SET, PAYLOAD_COMMAND_ACTIVITY_SET, PAYLOAD_COMMAND_VOICE_SETTINGS_SET, \
    PAYLOAD_COMMAND_VOICE_SETTINGS_GET, PAYLOAD_COMMAND_CHANNEL_TEXT_SELECT, PAYLOAD_COMMAND_CHANNEL_VOICE_GET, \
    PAYLOAD_COMMAND_CHANNEL_VOICE_SELECT, PAYLOAD_COMMAND_USER_VOICE_SETTINGS_SET, PAYLOAD_COMMAND_CHANNEL_GET, \
    PAYLOAD_COMMAND_GUILD_CHANNEL_GET_ALL, PAYLOAD_COMMAND_GUILD_GET, PAYLOAD_COMMAND_GUILD_GET_ALL, \
    PAYLOAD_COMMAND_AUTHENTICATE


def handle_command_dispatch(self, data):
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


def handle_command_forward_data(self, data):
    nonce = data.get(PAYLOAD_KEY_NONCE)
    if (nonce is None):
        return
    
    try:
        response_waiter = self._response_waiters[nonce]
    except KeyError:
        return
    
    payload_data = data.get(PAYLOAD_KEY_DATA, None)
    response_waiter.set_result_if_pending(payload_data)


COMMAND_HANDLERS = {
    PAYLOAD_COMMAND_DISPATCH: handle_command_dispatch,
    PAYLOAD_COMMAND_CERTIFIED_DEVICES_SET: handle_command_forward_data,
    PAYLOAD_COMMAND_ACTIVITY_SET: handle_command_forward_data,
    PAYLOAD_COMMAND_VOICE_SETTINGS_SET: handle_command_forward_data,
    PAYLOAD_COMMAND_VOICE_SETTINGS_GET: handle_command_forward_data,
    PAYLOAD_COMMAND_CHANNEL_TEXT_SELECT: handle_command_forward_data,
    PAYLOAD_COMMAND_CHANNEL_VOICE_GET: handle_command_forward_data,
    PAYLOAD_COMMAND_CHANNEL_VOICE_SELECT: handle_command_forward_data,
    PAYLOAD_COMMAND_USER_VOICE_SETTINGS_SET: handle_command_forward_data,
    PAYLOAD_COMMAND_GUILD_CHANNEL_GET_ALL: handle_command_forward_data,
    PAYLOAD_COMMAND_CHANNEL_GET: handle_command_forward_data,
    PAYLOAD_COMMAND_GUILD_GET: handle_command_forward_data,
    PAYLOAD_COMMAND_GUILD_GET_ALL: handle_command_forward_data,
    PAYLOAD_COMMAND_AUTHENTICATE: handle_command_forward_data,
}

del handle_command_dispatch
del handle_command_forward_data
