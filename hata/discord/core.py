__all__ = ('APPLICATION_COMMANDS', 'APPLICATIONS', 'CHANNELS', 'CLIENTS', 'DISCOVERY_CATEGORIES', 'EMOJIS', 'EULAS',
    'GUILDS', 'INTEGRATIONS', 'INVITES', 'KOKORO', 'MESSAGES', 'ROLES', 'STAGES', 'TEAMS', 'USERS', )

import sys, gc

from ..backend.utils import WeakValueDictionary, WeakKeyDictionary
from ..backend.event_loop import EventThread

CHANNELS = WeakValueDictionary()
CLIENTS = {}
EMOJIS = WeakValueDictionary()
GUILDS = WeakValueDictionary()
INTEGRATIONS = WeakValueDictionary()
MESSAGES = WeakValueDictionary()
ROLES = WeakValueDictionary()
TEAMS = WeakValueDictionary()
USERS = WeakValueDictionary()
DISCOVERY_CATEGORIES = WeakValueDictionary()
EULAS = WeakValueDictionary()
APPLICATIONS = WeakValueDictionary()
INVITES = WeakValueDictionary()
APPLICATION_COMMANDS = WeakValueDictionary()
INTERACTION_EVENT_RESPONSE_WAITERS = WeakValueDictionary()
INTERACTION_EVENT_MESSAGE_WAITERS = WeakKeyDictionary()
APPLICATION_ID_TO_CLIENT = {}
STAGES = WeakValueDictionary()

KOKORO = EventThread(daemon=False, name='KOKORO')

GC_CYCLER = KOKORO.cycle(1200.)

if sys.implementation.name == 'pypy':
    def manual_gc_call(cycler):
        gc.collect()
    
    GC_CYCLER.append(manual_gc_call, (1<<31)-1)
    
    del manual_gc_call
