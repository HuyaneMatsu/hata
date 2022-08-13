__all__ = ()

from functools import partial as partial_func
from re import (
    I as re_ignore_case, M as re_multi_line, S as re_dotall, compile as re_compile, escape as re_escape,
    match as re_match
)
from types import FunctionType

from scarletio import CallableAnalyzer, include

from ...discord.permission.permission import PERMISSION_CAN_SEND_MESSAGES_ALL

from .exceptions import CommandCheckError, CommandProcessingError
from .utils import raw_name_to_display


CheckBase = include('CheckBase')
CommandCheckWrapper = include('CommandCheckWrapper')

SUB_COMMAND_NAME_RP = re_compile('([a-zA-Z0-9_\-]+)\s*')
COMMAND_NAME_RP = re_compile('\s*([^\s]*)\s*', re_multi_line | re_dotall)

async def run_checks(checks, command_context):
    """
    Runs the checks.
    
    This function is coroutine.
    
    Parameters
    ----------
    checks : `GeneratorType`
        A generator yielding checks.
    command_context : ``CommandContext``
        The respective command's context.
    
    Returns
    -------
    failed : `None`, ``CheckBase``
        The failed check if any.
    
    Notes
    -----
    Not like ``handle_exception``, this can be called for checks of different commands.
    """
    for check in checks:
        if not await check(command_context):
            return check
    
    return None


async def handle_exception(command_context, exception):
    """
    Handles an exception raised meanwhile processing a command.
    
    This function is a coroutine.
    
    Parameters
    ----------
    command_context : ``CommandContext``
        The respective command context.
    exception : ``BaseException``
        The occurred exception.
    
    Returns
    -------
    invoked : `bool`
        Whether the command was successfully invoked.
        
        If unexpected exception occurs, still returns `True`.
    """
    command_function = command_context.command_function
    if (command_function is not None):
        for error_handler in command_function._iter_error_handlers():
            result = await error_handler(command_context, exception)
            if isinstance(result, int) and result:
                return True
    
    # We can ignore command processing exceptions.
    if isinstance(exception, CommandProcessingError):
        if isinstance(exception, CommandCheckError):
            return command_context.command.hidden_if_checks_fail
    else:
        client = command_context.client
        await client.events.error(client, 'handle_exception', exception)
    
    return True

def get_command_category_trace(command, content, index):
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
    command_category_trace : `None`, `tuple` of ``CommandCategory``
        Trace to the actual command.
    command_function : ``CommandFunction``, `None`
        The command function, which should be called.
    index : `int`
        The index till the command's parameters may start from.
    """
    command_category_name_to_command_category = command.command_category_name_to_command_category
    if (command_category_name_to_command_category is not None):
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
                command_category = command_category_name_to_command_category[name]
            except KeyError:
                break
            
            trace.append((end, command_category))
            
            sub_commands = command_category._command_categories
            if sub_commands is None:
                break
            
            continue
        
        while trace:
            end, command_category = trace[-1]
            command_function = command_category._command_function
            if (command_function is not None):
                return tuple(trace_element[1] for trace_element in trace), command_function, end
            
            del trace[-1]
            continue
    
    return None, command._command_function, index


def default_precheck(client, message):
    """
    Default check used by the command processor. Filters out every message what's author is a bot account and the
    channels where the client cannot send messages.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the respective message.
    message : ``Message``
        The received message.
    
    Returns
    -------
    should_process : `bool`
    """
    if message.author.bot:
        return False
    
    if not message.channel.cached_permissions_for(client) & PERMISSION_CAN_SEND_MESSAGES_ALL:
        return False
    
    return True


def test_precheck(precheck):
    """
    Tests whether the given precheck accepts the expected amount of parameters.
    
    Parameters
    ----------
    precheck : `callable`
        A function, which decides whether a received message should be processed.
        
        The following parameters are passed to it:
        
        +-----------+---------------+
        | Name      | Type          |
        +===========+===============+
        | client    | ``Client``    |
        +-----------+---------------+
        | message   | ``Message``   |
        +-----------+---------------+
        
        Should return the following parameters:
        
        +-------------------+-----------+
        | Name              | Type      |
        +===================+===========+
        | should_process    | `bool`    |
        +-------------------+-----------+
    
    Raises
    ------
    TypeError
        - If `precheck` accepts bad amount of parameters.
        - If `precheck` is async.
    """
    analyzer = CallableAnalyzer(precheck)
    if analyzer.is_async():
        raise TypeError(
            f'`precheck` should not be given as `async` function, got {precheck!r}.'
        )
    
    min_, max_ = analyzer.get_non_reserved_positional_parameter_range()
    if min_ > 2:
        raise TypeError(
            f'`precheck` should accept `2` parameters, meanwhile the given callable expects at '
            f'least `{min_!r}`, got {precheck!r}.'
        )
    
    if min_ != 2:
        if max_ < 2:
            if not analyzer.accepts_args():
                raise TypeError(
                    f'`precheck` should accept `2` parameters, meanwhile the given callable expects '
                    f'up to `{max_!r}`, got {precheck!r}.'
                )


def test_error_handler(error_handler):
    """
    Tests whether the given error handler accepts the expected amount of parameters.
    
    Parameters
    ----------
    error_handler : `callable`
        A function, which handles an error and returns whether handled it.
        
        The following parameters are passed to it:
        
        +-------------------+-----------------------+
        | Name              | Type                  |
        +===================+=======================+
        | command_context   | ``CommandContext``    |
        +-------------------+-----------------------+
        | exception         | `BaseException`       |
        +-------------------+-----------------------+
        
        Should return the following parameters:
        
        +-------------------+-----------+
        | Name              | Type      |
        +===================+===========+
        | handled           | `bool`    |
        +-------------------+-----------+
    
    Raises
    ------
    TypeError
        - If `error_handler` accepts bad amount of parameters.
        - If `error_handler` is not async.
    """
    analyzer = CallableAnalyzer(error_handler)
    if not analyzer.is_async():
        raise TypeError(
            f'`error_handler` can be `async` function, got {error_handler!r}'
        )
    
    min_, max_ = analyzer.get_non_reserved_positional_parameter_range()
    if min_ > 2:
        raise TypeError(
            f'`error_handler` should accept `2` parameters, meanwhile the given callable expects at '
            f'least `{min_!r}`, got {error_handler!r}'
        )
    
    if min_ != 2:
        if max_ < 2:
            if not analyzer.accepts_args():
                raise TypeError(
                    f'`error_handler` should accept `2` parameters, meanwhile the given callable expects '
                    f'up to `{max_!r}`, got {error_handler!r}.'
                )


def validate_error_handlers(error_handlers):
    """
    Validates the given error handlers.
    
    Parameters
    ----------
    error_handlers : `None`, `async-callable` or (`list`, `tuple`, `set`) of `async-callable`
        The error_handler(s) to validate.
    
    Returns
    -------
    error_handlers_validated : `None`, `list` of `async-callable`
        The validated error handlers.
    
    Raises
    ------
    TypeError
        - If `error_handler`'s type is incorrect.
        - If `error_handler` accepts bad amount of parameters.
        - If `error_handler` is not async.
    """
    error_handlers_validated = None
    
    if error_handlers is None:
        pass
    elif isinstance(error_handlers, (list, tuple, set)):
        for error_handler in error_handlers:
            test_error_handler(error_handler)
            
            if error_handlers_validated is None:
                error_handlers_validated = []
            
            error_handlers_validated.append(error_handler)
    else:
        test_error_handler(error_handlers)
        
        if error_handlers_validated is None:
            error_handlers_validated = []
        
        error_handlers_validated.append(error_handlers)
    
    return error_handlers_validated


def test_name_rule(rule, rule_name):
    """
    Tests the given name rule and raises if it do not passes any requirements.
    
    Parameters
    ----------
    rule : `None`, `function`
        The rule to test.
        
        A name rule should accept the following parameters:
        
        +-------+-------------------+
        | Name  | Type              |
        +=======+===================+
        | name  | `str`             |
        +-------+-------------------+
        
        Should return the following ones:
        
        +-------+-------------------+
        | Name  | Type              |
        +=======+===================+
        | name  | `str`             |
        +-------+-------------------+
    
    rule_name : `str`
        The name of the given rule.
    
    Raises
    ------
    TypeError
        - If `rule` is not `None`, `function`.
        - If `rule` is `async` `function`.
        - If `rule` accepts bad amount of parameters.
        - If `rule` raised exception when `str` was passed to it.
        - If `rule` did not return `str`, when passing `str` to it.
        - If `nullable` is given as `True` and `rule` raised exception when `None` was passed to it.
        - If `nullable` is given as `True` and `rule` did not return `str`, when passing `None` to it.
    """
    if rule is None:
        return
    
    rule_type = rule.__class__
    if (rule_type is not FunctionType):
        raise TypeError(
            f'`{rule_name}` can be `{FunctionType.__name__}`, got {rule_type.__name__}; {rule!r}.'
        )
    
    analyzed = CallableAnalyzer(rule)
    if analyzed.is_async():
        raise TypeError(
            f'`{rule_name}` can be a non async function, got {rule!r}.'
        )
    
    non_reserved_positional_parameter_count = analyzed.get_non_reserved_positional_parameter_count()
    if non_reserved_positional_parameter_count != 1:
        raise TypeError(
            f'`{rule_name}` should accept `1` non reserved positional parameters, meanwhile it expects '
            f'{non_reserved_positional_parameter_count}, got {rule!r}.'
        )
    
    if analyzed.accepts_args():
        raise TypeError(
            f'`{rule_name}` should accept not expect args, meanwhile it does, got {rule!r}.'
        )
    
    if analyzed.accepts_kwargs():
        raise TypeError(
            f'`{rule_name}` should accept not expect kwargs, meanwhile it does, got {rule!r}.'
        )
    
    non_default_keyword_only_parameter_count = analyzed.get_non_default_keyword_only_parameter_count()
    if non_default_keyword_only_parameter_count:
        raise TypeError(
            f'`{rule_name}` should accept `0` keyword only parameters, meanwhile it expects '
            f'{non_default_keyword_only_parameter_count}, got {rule!r}.'
        )
    
    try:
        result = rule('test-this-name')
    except BaseException as err:
        raise TypeError(
            f'Got unexpected exception meanwhile testing the given {rule_name}: {rule!r}.'
        ) from err
    
    if (type(result) is not str):
        raise TypeError(
            f'{rule_name}: {rule!r} did not return `str`, meanwhile testing it, got {result.__class__.__name__}.'
        )


def validate_category_or_command_name(name):
    """
    Validates the given category name.
    
    Parameters
    ----------
    name : `str`
        The name of a category or command.
    
    Returns
    -------
    name : `str`
        The validated name.
    
    Raises
    ------
    TypeError
        If `name` was not given as `str`.
    ValueError
        If `name`'s length is out of range [1:128] characters.
    """
    name_type = type(name)
    if name_type is str:
        pass
    elif issubclass(name_type, str):
        name = str(name)
    else:
        raise TypeError(
            f'Category and command names can be `str`, got {name_type.__name__}; {name!r}.'
        )
    
    name_length = len(name)
    if (name_length < 1) or (name_length > 128):
        raise ValueError(
            f'`Category and command name length can be in range [0:128], got {name_length}; {name!r}.'
        )
    
    return name


async def prefix_wrapper_async_callable(prefix_factory, re_flags, message):
    """
    Function to execute asynchronous callable prefix.
    
    This function is a coroutine.
    
    Parameters
    ----------
    prefix_factory : `async-callable`
        Async callable returning the prefix.
    re_flags : `int`
        Regex matching flags.
    message : ``Message``
        The received message to parse the prefix from.
    
    Returns
    -------
    prefix : `None`, `str`
        The prefix used by the user. Returned as `None` of parsing failed.
    end : `int`
        The start of the content after the prefix. Returned as `-1` if parsing failed.
    """
    prefix = await prefix_factory(message)
    if isinstance(prefix, str):
        escaped_prefix = re_escape(prefix)
    elif isinstance(prefix, tuple) and (len(prefix) > 0):
        escaped_prefix = '|'.join(re_escape(prefix_part) for prefix_part in prefix)
    else:
        return None, -1
    
    content = message.content
    if content is None:
        prefix = None
        end = -1
    else:
        parsed = re_match(escaped_prefix, content, re_flags)
        if parsed is None:
            prefix = None
            end = -1
        else:
            prefix = parsed.group(0)
            end = parsed.end()
    
    return prefix, end


async def prefix_getter_async_callable(prefix_factory, message):
    """
    Returns a prefix for the message.
    
    This function is a coroutine.
    
    Parameters
    ----------
    prefix_factory : `async-callable`
        Async callable returning the prefix.
    message : ``Message``
        The received message to parse the prefix from.
    
    Returns
    -------
    prefix : `None`, `str`
        The respective prefix for the message. Returns `None` of non could be identified.
    """
    prefix = await prefix_factory(message)
    if isinstance(prefix, str):
        pass
    elif isinstance(prefix, tuple) and (len(prefix) > 0):
        prefix = prefix[0]
    else:
        prefix = None
    
    return prefix


async def prefix_wrapper_sync_callable(prefix_factory, re_flags, message):
    """
    Function to execute not asynchronous callable prefix.
    
    This function is a coroutine.
    
    Parameters
    ----------
    prefix_factory : `async-callable`
        Async callable returning the prefix.
    re_flags : `int`
        Regex matching flags.
    message : ``Message``
        The received message to parse the prefix from.
    
    Returns
    -------
    prefix : `None`, `str`
        The prefix used by the user. Returned as `None` of parsing failed.
    end : `int`
        The start of the content after the prefix. Returned as `-1` if parsing failed.
    """
    prefix = prefix_factory(message)
    if isinstance(prefix, str):
        escaped_prefix = re_escape(prefix)
    elif isinstance(prefix, tuple) and (len(prefix) > 0):
        escaped_prefix = '|'.join(re_escape(prefix_part) for prefix_part in prefix)
    else:
        return None, -1
    
    content = message.content
    if content is None:
        prefix = None
        end = -1
    else:
        parsed = re_match(escaped_prefix, content, re_flags)
        if parsed is None:
            prefix = None
            end = -1
        else:
            prefix = parsed.group(0)
            end = parsed.end()
    
    return prefix, end


async def prefix_getter_sync_callable(prefix_factory, message):
    """
    Returns a prefix for the message.
    
    This function is a coroutine.
    
    Parameters
    ----------
    prefix_factory : `callable`
        Sync callable returning the prefix.
    message : ``Message``
        The received message to parse the prefix from.
    
    Returns
    -------
    prefix : `None`, `str`
        The respective prefix for the message. Returns `None` of non could be identified.
    """
    prefix = prefix_factory(message)
    if isinstance(prefix, str):
        pass
    elif isinstance(prefix, tuple) and (len(prefix) > 0):
        prefix = prefix[0]
    else:
        prefix = None
    
    return prefix


async def prefix_wrapper_regex(re_pattern, message):
    """
    Function to execute asynchronous callable prefix.
    
    This function is a coroutine.
    
    Parameters
    ----------
    re_pattern : `async-callable`
        Async callable returning the prefix.
    message : ``Message``
        The received message to parse the prefix from.
    
    Returns
    -------
    prefix : `None`, `str`
        The prefix used by the user. Returned as `None` of parsing failed.
    end : `int`
        The start of the content after the prefix. Returned as `-1` if parsing failed.
    """
    content = message.content
    if content is None:
        prefix = None
        end = -1
    else:
        parsed = re_pattern.match(content)
        if parsed is None:
            prefix = None
            end = -1
        else:
            prefix = parsed.group(0)
            end = parsed.end()
    
    return prefix, end


async def prefix_getter_static(prefix, message):
    """
    Returns a prefix for the message.
    
    This function is a coroutine.
    
    Parameters
    ----------
    prefix : `str`
        The prefix to return.
    message : ``Message``
        The received message to parse the prefix from.
    
    Returns
    -------
    prefix : `str`
        The respective prefix for the message.
    """
    return prefix


def get_prefix_parser(prefix, prefix_ignore_case):
    """
    Validates whether the given prefix is correct.
    
    Parameters
    ----------
    prefix :  `str`, `tuple` of `str`, `callable`
        Prefix of the command processor.
        
        Can be given as a normal `callable` or as an `async-callable` as well, which should accept `1` parameter:
        
        +-------------------+---------------+
        | Name              | Type          |
        +===================+===============+
        | message           | ``Message``   |
        +-------------------+---------------+
        
        And return the following value:
        
        +-------------------+---------------------------+
        | Name              | Type                      |
        +===================+===========================+
        | prefix            | `str`, `tuple` of `str`   |
        +-------------------+---------------------------+
    
    Returns
    -------
    prefix_parser : `async-callable`
        Async callable prefix parser.
        
        Accepts the following parameters:
        
        +-----------+---------------+
        | Name      | Type          |
        +===========+===============+
        | message   | ``Message``   |
        +-----------+---------------+
        
        Returns the given values:
        
        +-----------+-------------------+
        | Name      | Type              |
        +===========+===================+
        | prefix    | `None`, `str`     |
        +-----------+-------------------+
        | end       | `int`             |
        +-----------+-------------------+
    
    prefix_getter : `async-callable`
        
        Accepts the following parameters:
        
        +-----------+---------------+
        | Name      | Type          |
        +===========+===============+
        | message   | ``Message``   |
        +-----------+---------------+
        
        Returns the given values:
        
        +-----------+-------------------+
        | Name      | Type              |
        +===========+===================+
        | prefix    | `None`, `str`     |
        +-----------+-------------------+
    
    Raises
    ------
    TypeError
        - Prefix's type is incorrect.
        - Prefix is a callable but accepts bad amount of parameters.
    """
    if prefix_ignore_case:
        re_flags = re_ignore_case
    else:
        re_flags = 0
    
    re_flags |= re_multi_line | re_dotall
    
    if callable(prefix):
        analyzed = CallableAnalyzer(prefix)
        non_reserved_positional_parameter_count = analyzed.get_non_reserved_positional_parameter_count()
        if non_reserved_positional_parameter_count != 1:
            raise TypeError(
                f'Callable `prefix` should accept `1` non reserved positional parameter, meanwhile it '
                f'accepts: {non_reserved_positional_parameter_count}, got {prefix!r}.'
            )
        
        if analyzed.is_async():
            prefix_wrapper_function = prefix_wrapper_async_callable
            prefix_getter_function = prefix_getter_async_callable
        else:
            prefix_wrapper_function = prefix_wrapper_sync_callable
            prefix_getter_function = prefix_getter_sync_callable
        
        prefix_parser = partial_func(prefix_wrapper_function, prefix, re_flags)
        prefix_getter = partial_func(prefix_getter_function, prefix)
    
    else:
        if isinstance(prefix, str):
            escaped_prefix = re_escape(prefix)
        elif isinstance(prefix, tuple):
            if len(prefix) == 0:
                raise ValueError(
                    f'`prefix` cannot be an empty `tuple`.'
                )
            
            escaped_prefix = '|'.join(re_escape(prefix_part) for prefix_part in prefix)
            prefix = prefix[0]
        else:
            raise TypeError(
                f'`prefix` can be `callable`, `async-callable`, `str`, `tuple` of `str`, got '
                f'{prefix.__class__.__name__}; {prefix!r}.'
            )
        
        compiled_prefix = re_compile(escaped_prefix, re_flags)
        
        prefix_parser = partial_func(prefix_wrapper_regex, compiled_prefix)
        prefix_getter = partial_func(prefix_getter_static, prefix)
    
    return prefix_parser, prefix_getter


def _unwrap_check(check):
    """
    Unwraps the given check if applicable.
    
    Parameters
    ----------
    check : ``CheckBase``, ``CommandCheckWrapper``
        The check to unwrap.
    
    Returns
    -------
    check : ``CheckBase``
        The unwrapped check.
    
    Raises
    ------
    TypeError
        If `check` is neither ``CheckBase`` nor ``CommandCheckWrapper``.
    """
    if isinstance(check, CheckBase):
        return check
    
    if isinstance(check, CommandCheckWrapper):
        return check._check
    
    raise TypeError(
        f'`check` can be `{CheckBase.__name__}`, `{CommandCheckWrapper.__name__}`, got '
        f'{check.__class__.__name__}; {check!r}.'
    )


def validate_checks(checks):
    """
    Validates the given checks.
    
    Parameters
    ----------
    checks : `None`, ``CheckBase``, ``CommandCheckWrapper`` or (`list`, `tuple`, `set`) of \
            (``CheckBase``, ``CommandCheckWrapper``)
        The check(s) to validate.
    
    Returns
    -------
    checks_validated : `None`, `tuple` of ``CheckBase``
        The validated checks.
    
    Raises
    ------
    TypeError
        - If `checks`'s type is incorrect.
        - If a `check`'s type is incorrect.
    """
    checks_validated = None
    
    if checks is None:
        pass
    elif isinstance(checks, (list, tuple, set)):
        for check in checks:
            check = _unwrap_check(check)
            
            if checks_validated is None:
                checks_validated = []
            
            checks_validated.append(check)
        
        checks = tuple(checks_validated)
    else:
        check = _unwrap_check(checks)
        
        checks = (check, )
    
    return checks


def test_unknown_command(unknown_command):
    """
    Tests whether the given unknown command handler accepts the expected amount of parameters.
    
    Parameters
    ----------
    unknown_command : `callable`
        A function, which is called when no command is found.
        
        The following parameters are passed to it:
        
        +---------------+---------------+
        | Name          | Type          |
        +===============+===============+
        | client        | ``Client``    |
        +---------------+---------------+
        | message       | ``Message``   |
        +---------------+---------------+
        | command_name  | `str`         |
        +---------------+---------------+
    
    Raises
    ------
    TypeError
        - If `unknown_command` accepts bad amount of parameters.
        - If `unknown_command` is not async.
    """
    analyzer = CallableAnalyzer(unknown_command)
    if not analyzer.is_async():
        raise TypeError(
            f'`unknown_command` can be `async` function, got {unknown_command!r}.'
        )
    
    min_, max_ = analyzer.get_non_reserved_positional_parameter_range()
    if min_ > 3:
        raise TypeError(
            f'`unknown_command` should accept `2` parameters, meanwhile the given callable expects at '
            f'least `{min_!r}`, got {unknown_command!r}.'
        )
    
    if min_ != 3:
        if max_ < 3:
            if not analyzer.accepts_args():
                raise TypeError(
                    f'`unknown_command` should accept `2` parameters, meanwhile the given callable expects '
                    f'up to `{max_!r}`, got {unknown_command!r}.'
                )
