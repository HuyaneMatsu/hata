# -*- coding: utf-8 -*-
import sys, warnings
from types import ModuleType

from . import asyncio

try:
    module = sys.modules['asyncio']
except KeyError:
    module = asyncio
    sys.modules['asyncio'] = asyncio

else:
    warnings.warn(f'asyncio is already loaded, replacing it.')
    
    try:
        del sys.modules['_asyncio']
    except KeyError:
        pass
    
    module.__dict__.clear()
    module.__dict__.update(asyncio.__dict__)

module.__file__ = __file__

sys.modules[__name__] = asyncio

for sub_module_name, feature_names, extra_features in (
        ('base_events', (
            'BaseEventLoop',
            '_run_until_complete_cb', # Required by anyio
            ), None,
        ),
        ('base_futures', None, None),
        ('base_subprocess', None, None),
        ('base_tasks', None, None),
        ('constants', None, None),
        ('coroutines', (
            'coroutine',
            'iscoroutinefunction',
            'iscoroutine',
            ), (
            ('_DEBUG', False), # Required by aiohttp 3.8
            )
        ),
        ('events', (
            'AbstractEventLoopPolicy',
            'AbstractEventLoop',
            'AbstractServer',
            'Handle',
            'TimerHandle',
            'get_event_loop_policy',
            'set_event_loop_policy',
            'get_event_loop',
            'set_event_loop',
            'new_event_loop',
            'get_child_watcher',
            'set_child_watcher',
            '_set_running_loop',
            'get_running_loop',
            '_get_running_loop',
            ), None,
        ),
        ('exceptions', (
            'CancelledError',
            'InvalidStateError',
            'TimeoutError',
            'IncompleteReadError',
            'LimitOverrunError',
            'SendfileNotAvailableError',
            ), None,
        ),
        ('format_helpers', None, None),
        ('futures', (
            'Future',
            'wrap_future',
            'isfuture',
            ), None,
        ),
        ('locks', (
            'Lock',
            'Event',
            'Condition',
            'Semaphore',
            'BoundedSemaphore',
            ), None,
        ),
        ('proactor_events', (
            'BaseProactorEventLoop',
            ), None,
        ),
        ('protocols', (
            'BaseProtocol',
            'Protocol',
            'DatagramProtocol',
            'SubprocessProtocol',
            'BufferedProtocol',
            ), None,
        ),
        ('queues', (
            'Queue',
            'PriorityQueue',
            'LifoQueue',
            'QueueFull',
            'QueueEmpty',
            ), None,
        ),
        ('runners', (
            'run',
            ), None,
        ),
        ('selector_events', (
            'BaseSelectorEventLoop',
            ), None,
        ),
        ('sslproto', None, None),
        ('staggered_race', (
            'staggered_race',
            ), None,
        ),
        ('streams', (
            'StreamReader',
            'StreamWriter',
            'StreamReaderProtocol',
            'open_connection',
            'start_server',
            ), None,
        ),
        ('subprocess', (
            'create_subprocess_exec',
            'create_subprocess_shell',
            'Process', # Required by anyio
            ), None,
        ),
        ('tasks', (
            'Task',
            'create_task',
            'FIRST_COMPLETED',
            'FIRST_EXCEPTION',
            'ALL_COMPLETED',
            'wait',
            'wait_for',
            'as_completed',
            'sleep',
            'gather',
            'shield',
            'ensure_future',
            'run_coroutine_threadsafe',
            'current_task',
            'all_tasks',
            '_register_task',
            '_unregister_task',
            '_enter_task',
            '_leave_task',
            ), None,
        ),
        ('threads', (
            'to_thread',
            ), None,
        ),
        ('transports', (
            'BaseTransport',
            'ReadTransport',
            'WriteTransport',
            'Transport',
            'DatagramTransport',
            'SubprocessTransport',
            ), None,
        ),
        ('trsock', None, None),
        ('unix_events', (
            'SelectorEventLoop',
            'AbstractChildWatcher',
            'SafeChildWatcher',
            'FastChildWatcher',
            'PidfdChildWatcher',
            'MultiLoopChildWatcher',
            'ThreadedChildWatcher',
            'DefaultEventLoopPolicy',
            ), None,
        ),
        ('windows_events', (
            'SelectorEventLoop',
            'ProactorEventLoop',
            'IocpProactor',
            'DefaultEventLoopPolicy',
            'WindowsSelectorEventLoopPolicy',
            'WindowsProactorEventLoopPolicy',
            ), None,
        ),
        ('windows_utils', (
            'pipe',
            'Popen',
            'PIPE',
            'PipeHandle',
            ), None,
        )
            ):
    
    module_name = f'asyncio.{sub_module_name}'
    
    try:
        module = sys.modules[module_name]
    except KeyError:
        module = ModuleType(module_name)
        sys.modules[module_name] = module
    else:
        module.__dict__.clear()
    
    asyncio.__dict__[sub_module_name] = module
    module.__file__ = __file__
    
    if (feature_names is not None):
        module.__all__ = feature_names
        module.__dict__.update((feature_name, getattr(asyncio, feature_name)) for feature_name in feature_names)
    
    if (extra_features is not None):
        module.__dict__.update(extra_features)

del extra_features
del sub_module_name
del feature_names
del module_name
del module
del asyncio

from .. import register_library_extension
register_library_extension('HuyaneMatsu.asyncio')
del register_library_extension
