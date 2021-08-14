import sys, warnings
from code import InteractiveConsole
from functools import partial as partial_func
from types import FunctionType
try:
    import readline
except ImportError:
    pass
from .. import Future, EventThread, is_awaitable, __package__ as PACKAGE_NAME

PACKAGE = __import__(PACKAGE_NAME)

# If only hata backend is imported, KOKORO is not present.
try:
    from .. import KOKORO as EVENT_LOOP
except ImportError:
    EVENT_LOOP = EventThread(daemon=False)

# On python3.6 not present?
try:
    from ast import PyCF_ALLOW_TOP_LEVEL_AWAIT
except ImportError:
    PyCF_ALLOW_TOP_LEVEL_AWAIT = 1<<13
    AWAIT_AVAILABLE = False
else:
    AWAIT_AVAILABLE = True


def run_code_callback(console, code):
    function = FunctionType(code, console.locals)
    try:
        coroutine = function()
    except BaseException as err:
        if isinstance(err, KeyboardInterrupt):
            console.interrupted = True
        
        console.future.set_exception(err)
        return
    
    if not is_awaitable(coroutine):
        console.future.set_result(coroutine)
        return
    
    try:
        task = EVENT_LOOP.ensure_future(coroutine)
    except BaseException as err:
        console.future.set_exception(err)
    else:
        console.future.set_result(None)
        console.task = task


class AsynchronousInteractiveConsole(InteractiveConsole):
    
    def __init__(self, locals):
        InteractiveConsole.__init__(self, locals)
        self.compile.compiler.flags |= PyCF_ALLOW_TOP_LEVEL_AWAIT
        
        self.future = None
        self.interrupted = False
        self.task = None
    
    def runcode(self, code):
        self.future = Future(EVENT_LOOP)
        self.interrupted = False
        self.task = None
        
        EVENT_LOOP.call_soon_thread_safe(partial_func(run_code_callback, self, code))
        
        try:
            result = self.future.sync_wrap().wait()
            
            task = self.task
            if (task is not None):
                result = task.sync_wrap().wait()
        
        except BaseException as err:
            future = self.future
            if (not future.done()):
                future.cancel()
            
            task = self.task
            if (task is not None) and (not task.done()):
                task.cancel()
            
            if isinstance(err, SystemExit):
                raise
            
            if self.interrupted:
                self.write('\nKeyboardInterrupt\n')
            else:
                self.showtraceback()
        else:
            return result

if AWAIT_AVAILABLE:
    AWAIT_NOTE = 'Use \'await\' directly.'
else:
    AWAIT_NOTE = '!!! Direct \'await\' is not available on your python version. Please use python 3.8 or newer !!!'

NAME = 'interpreter'
USAGE = 'i | interpreter'

HELP = (
    f'Runs asynchronous python interpreter through hata\'s asynchronous environment.\n'
    f'{AWAIT_NOTE}\n'
)

def __main__():
    interactive_console_locals = {PACKAGE_NAME: PACKAGE}
    for variable_name in {
            '__name__',
            '__package__',
            '__loader__',
            '__spec__',
            '__builtins__',
            '__file__'
                }:
        interactive_console_locals[variable_name] = getattr(PACKAGE, variable_name)
    
    for variable_name in PACKAGE.__all__:
        interactive_console_locals[variable_name] = getattr(PACKAGE, variable_name)
    

    
    banner = (
        f'{PACKAGE_NAME} interactive_console {sys.version} on {sys.platform}.\n'
        f'{AWAIT_NOTE}\n'
        f'Type \'help\', \'copyright\', \'credits\' or \'license\' for more information.'
    )
    
    exit_message = f'exiting {PACKAGE_NAME} interactive_console...'
    
    console = AsynchronousInteractiveConsole(interactive_console_locals)
    
    try:
        console.interact(
            banner = banner,
            exitmsg = exit_message,
        )
    finally:
        warnings.filterwarnings(
            'ignore',
            message = r'^coroutine .* was never awaited$',
            category = RuntimeWarning,
        )
        
        EVENT_LOOP.stop()
