import re

from .utils import raw_name_to_display

SUB_COMMAND_NAME_RP = re.compile('([a-zA-Z0-9_\-]+)\S*')

async def run_checks(checks, command_context):
    """
    Runs the checks.
    
    This function is coroutine.
    
    Parameters
    ----------
    checks : `generator`
        A generator yielding checks.
    command_context : ``CommandContext``
        The respective command's context.
    
    Returns
    -------
    failed : `None` or ``CheckBase``
        The failed check if any.
    """
    for check in checks:
        if not await check(command_context):
            return check
    
    return None

    
async def handle_exception(error_handlers, command_context, exception):
    """
    Handles an exception raised meanwhile processing a command.
    
    This function is a coroutine.
    
    Parameters
    ----------
    error_handlers : `generator`
        A generator yielding error checks.
    command_context : ``CommandContext``
        The respective command context.
    exception : ``BaseException``
        The occurred exception.
    """
    for error_handler in error_handlers:
        result = await error_handler(command_context, exception)
        if isinstance(result, int) and result:
            break
    else:
        client = command_context.client
        await client.events.error(client, '_handle_exception', exception)

    
def get_sub_command_trace(command, content, index):
    """
    Gets the sub command trace and command function for the given command.
    
    Parameters
    ----------
    command : ``Command``
        The respective command.
    content : `str`
        A message's content to parse.
    index : `int`
        The starting index from where the content should be parsed from.
    
    Returns
    -------
    sub_command_trace : `None` or `tuple` of ``CommandCategory``
        Trace to the actual command.
    command_function : ``CommandFunction`` or `None`
        The command function, which should be called.
    index : `int`
        The index till the command's parameters may start from.
    """
    sub_commands = command._sub_commands
    if (sub_commands is not None):
        trace = []
        end = index
        while True:
            if end == len(content):
                break
            
            parsed = SUB_COMMAND_NAME_RP.match(content, end)
            if (parsed is None):
                break
            
            end = parsed.end()
            part = parsed.group(1)
            name = raw_name_to_display(part)
            
            try:
                sub_command = sub_commands[name]
            except KeyError:
                break
            
            trace.append((end, sub_command))
            
            sub_commands = sub_command._sub_commands
            if sub_commands is None:
                break
            
            continue
        
        while trace:
            end, sub_command = trace[-1]
            command_function = sub_command._command
            if (command_function is not None):
                return tuple(trace_element[1] for trace_element in trace), command_function, end
            
            del trace[-1]
            continue
    
    return None, command.command_function, index



