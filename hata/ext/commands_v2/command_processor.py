__all__ = ('CommandProcessor', )

from ...backend.utils import WeakReferer
from ...discord.parsers import EventWaitforBase
from ...discord.preconverters import preconvert_bool
from ...discord.utils import USER_MENTION_RP

from .command_helpers import default_precheck, test_precheck, test_error_handler, test_name_rule, \
    validate_category_or_command_name, get_prefix_parser, COMMAND_NAME_RP, raw_name_to_display
from .context import CommandContext
from .category import CommandCategory

DEFAULT_CATEGORY_NAME = 'UNCATEGORIZED'

class CommandProcessor(EventWaitforBase):
    """
    Command processor.
    
    
    Attributes
    ----------
    _category_name_rule : `None` or `function`
        Function to generate category display names.
        
        A category name rule should accept the following parameters:
        
        +-------+-------------------+
        | Name  | Type              |
        +=======+===================+
        | name  | `None` or `str`   |
        +-------+-------------------+
        
        Should return the following ones:
        
        +-------+-------------------+
        | Name  | Type              |
        +=======+===================+
        | name  | `str`             |
        +-------+-------------------+
    
    _command_name_rule : `None` or `function`
        Function to generate command display names.
        
        A command name rule should accept the following parameters:
        
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
    
    _default_category : ``CommandCategory``
        The command processor's default category.
    
    _error_handlers : `None` or `list` of `async-function`
        Function to run when a command raises an exception.
        
        The following parameters are passed to each error handler:
        
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
    
    _mention_prefix_enabled : `bool`
        Whether mentioning the client at the start of a message counts as prefix.
    
    _precheck : `function`
        A function used to detect whether a message should be handled.
        
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
    
    _prefix_getter : `async-callable`
        
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
        | prefix    | `None` or `str`   |
        +-----------+-------------------+
    
    _prefix_ignore_case : `bool`
        Whether casing in prefix is ignored.
    
    _prefix_parser : `async-callable`
        Parses the prefix down from a message's start.
        
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
        | prefix    | `None` or `str`   |
        +-----------+-------------------+
        | end       | `int`             |
        +-----------+-------------------+
    
    _prefix_raw : `str`, `tuple` of `str`, `callable`
        Raw prefix of the command processor.
    
    _self_reference : `None` or ``WeakReferer`` to ``CommandProcessor``
        Reference to the command processor itself.
    
    categories_name_to_categories : `dict` of (`str`, ``CommandCategory``) items
        Category name to category relation.
    
    command_name_to_command : `dict` of (`str`, ``Command``) items
        Command name to command relation.
    
    Notes
    -----
    ``CommandProcessor`` supports weakreferencing.
    """
    
    __slots__ = ('__weakref__', '_category_name_rule', '_command_name_rule', '_default_category',
        '_error_handlers', '_mention_prefix_enabled', '_precheck', '_prefix_getter', '_prefix_ignore_case',
        '_prefix_parser', '_prefix_raw', '_self_reference', 'categories_name_to_categories',
        'command_name_to_command')
    
    def __new__(cls, prefix, *, precheck=None, mention_prefix_enabled=True, category_name_rule=None,
            command_name_rule=None, default_category_name=None, prefix_ignore_case=True):
        """
        Creates a new command processor instance.
        
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
            
        precheck : `bool`, Optional (Keyword only)
            A function used to detect whether a message should be handled.
        mention_prefix_enabled : `bool`, Optional (Keyword only)
            Whether mentioning the client at the start of a message counts as prefix. Defaults to `True`.
        category_name_rule : `None` or `function`, Optional (Keyword only)
            Function to generate category display names. Defaults to `None`.
        command_name_rule : `None` or `function`, Optional (Keyword only)
            Function to generate command display names. Defaults to `None`.
        default_category_name : `str` or `None`, Optional (Keyword only)
            The command processor's default category's name. Defaults to `None`.
        prefix_ignore_case : `bool`
            Whether the prefix's case should be ignored.
        
        Raises
        ------
        TypeError
            - If `precheck` accepts bad amount of arguments.
            - If `precheck` is async.
            - If `mention_prefix_enabled` was not given as a `bool` instance.
            - If `category_name_rule` is not `None` nor `function`.
            - If `category_name_rule` is `async-function`.
            - If `category_name_rule` accepts bad amount of parameters.
            - If `category_name_rule` raises exception when `str` or `None` is passed to it.
            - If `category_name_rule` not returns `str`, when passing `str` or `None` to it.
            - If `command_name_rule` is not `None` nor `function`.
            - If `command_name_rule` is `async-function`.
            - If `command_name_rule` accepts bad amount of parameters.
            - If `command_name_rule` raises exception when `str` is passed to it.
            - If `command_name_rule` not returns `str`, when `str` is passed to it.
            - If `default_category_name` was not given neither as `None` nor as `str` instance.
            - If `prefix_ignore_case` was not given as `bool` instance.
            - Prefix's type is incorrect.
            - Prefix is a callable but accepts bad amount of parameters.
        ValueError
            - If `default_category_name`'s length is out of range [1:128].
        """
        if (category_name_rule is not None):
            test_name_rule(category_name_rule, 'category_name_rule', True)
        
        if (command_name_rule is not None):
            test_name_rule(command_name_rule, 'command_name_rule', False)
        
        if default_category_name is None:
            default_category_name = DEFAULT_CATEGORY_NAME
        else:
            default_category_name = validate_category_or_command_name(default_category_name)
        
        if (category_name_rule is not None):
            default_category_name = category_name_rule(default_category_name)
        
        default_category = CommandCategory(default_category_name)
        
        if precheck is None:
            precheck = default_precheck
        else:
            test_precheck(precheck)
        
        mention_prefix_enabled = preconvert_bool(mention_prefix_enabled, 'mention_prefix_enabled')
        prefix_ignore_case = preconvert_bool(prefix_ignore_case, 'prefix_ignore_case')
        
        prefix_parser, prefix_getter = get_prefix_parser(prefix, prefix_ignore_case)
        
        self = object.__new__(cls)
        self._self_reference = None
        self._precheck = precheck
        self._error_handlers = None
        self._mention_prefix_enabled = mention_prefix_enabled
        self._category_name_rule = category_name_rule
        # Assign it later, exception may occur
        self._self_reference = WeakReferer(self)
        self._prefix_ignore_case = prefix_ignore_case
        self._prefix_parser = prefix_parser
        self._prefix_raw = prefix
        self._prefix_getter = prefix_getter
        self._default_category = default_category
        self._command_name_rule = command_name_rule
        self._category_name_rule = category_name_rule
        self.command_name_to_command = {}
        self.categories_name_to_categories = {default_category.name: default_category}
        
        self._self_reference = WeakReferer(self)
        
        default_category.set_command_processor(self)
        
        return self
    
    async def __call__(self, client, message):
        """
        Calls the waitfors of the command processor, processing the given `message`'s content, and calls a command if
        found, or an other specified event.
        
        Details under ``CommandProcessor``'s own docs.
        
        This method is a coroutine.
        
        Arguments
        ---------
        client : ``Client``
            The client, who received the message.
        message : ``Message``
            The received message.
        """
        await self.call_waitfors(client, message)
        
        if not self._precheck(client, message):
            return
        
        prefix, end = self._prefix_parser(message)
        if (prefix is None):
            if not self._mention_prefix_enabled:
                return
            
            user_mentions = message.user_mentions
            if (user_mentions is None) or (client not in user_mentions):
                return
            
            parsed = USER_MENTION_RP.match(message.content)
            if (parsed is None) or (int(parsed.group(1)) != client.id):
                return
            
            end = parsed.end()
        
        parsed = COMMAND_NAME_RP.match(message.content, end)
        if (parsed is None):
            return
        
        command_name = parsed.group(1)
        end = parsed.end()
        
        command_name = raw_name_to_display(command_name)
        
        try:
            command = self.command_name_to_command[command_name]
        except KeyError:
            # do later, character lazy
            return
        
        content = message.content[end:]
        
        context = CommandContext(client, message, prefix, content, command)
        await context.invoke()
    
    
    def error(self, error_handler):
        """
        Adds na error handler to the command processor.
        
        Parameters
        ----------
        error_handler : `async-callable`
            The error handler to add.
            
            The following parameters are passed to each error handler:
            
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
        
        Returns
        -------
        error_handler : `async-callable`
        
        Raises
        ------
        TypeError
            - If `error_handler` accepts bad amount of arguments.
            - If `error_handler` is not async.
        """
        test_error_handler(error_handler)
        
        error_handlers = self._error_handlers
        if error_handlers is None:
            error_handlers = self._error_handlers = []
            
            error_handlers.append(error_handler)
        
        return error_handler
    
    
    def update_prefix(self, *, prefix=None, prefix_ignore_case=None):
        """
        Updates the prefix of he
        
        Returns
        -------
        prefix :  `str`, `tuple` of `str`, `callable`, Optional (Keyword only)
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
        
        prefix_ignore_case : `bool`, Optional (Keyword only)
            Whether the prefix's case should be ignored.
        
        Raises
        ------
        TypeError
            - If `prefix_ignore_case` was not given as `bool` instance.
            - Prefix's type is incorrect.
            - Prefix is a callable but accepts bad amount of parameters.
        """
        if (prefix is None) and (prefix_ignore_case is None):
            return
        
        if prefix is None:
            prefix = self._prefix_raw
        
        if prefix_ignore_case is None:
            prefix_ignore_case = self._prefix_ignore_case
        
        prefix_ignore_case = preconvert_bool(prefix_ignore_case, 'prefix_ignore_case')
        
        prefix_parser, prefix_getter = get_prefix_parser(prefix, prefix_ignore_case)
        
        self._prefix_ignore_case = prefix_ignore_case
        self._prefix_parser = prefix_parser
        self._prefix_raw = prefix
        self._prefix_getter = prefix_getter
    
    
    async def get_prefix(self, message):
        """
        Gets prefix relating to the given message.
        
        This method is a coroutine.
        
        Parameters
        ----------
        message : ``Message``
            The respective message.
        
        Returns
        -------
        prefix : `str` or `None`
        """
        return await self._prefix_getter(message)
    
    
    def get_category(self, category_name):
        """
        Returns the category for the given name. If the name is passed as `None`, then will return the default category
        of the command processer.
        
        Returns `None` if there is no category with the given name.
        
        Parameters
        ---------
        category_name : `str` or `None`
            The category's name.
        
        Returns
        -------
        category : `None`, ``CommandCategory``
        
        Raises
        ------
        TypeError
            If `category_name` was not given neither as  `None` or `str` instance.
        """
        if category_name is None:
            return self._default_category
        
        if not isinstance(category_name, str):
            raise TypeError(f'`category_name` can be given as `None` or as `str` instance, got '
                f'{category_name.__class__.__name__}.')
        
        category_name = raw_name_to_display(category_name)
        
        return self.categories_name_to_categories.get(category_name, None)
    
    
    def get_default_category(self):
        """
        Returns the command processor's default category.
        
        Returns
        -------
        category : ``CommandCategory``
        """
        return self._default_category


