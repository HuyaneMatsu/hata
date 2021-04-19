__all__ = ('CommandProcessor', )

from ...backend.utils import WeakReferer
from ...discord.parsers import EventWaitforBase
from ...discord.preconverters import preconvert_bool

from .command_helpers import default_precheck, test_precheck, test_error_handler, test_name_rule, \
    validate_category_or_command_name

DEFAULT_CATEGORY_NAME = 'UNCATEGORIZED'

class CommandProcessor(EventWaitforBase):
    """
    Command processor.
    
    
    Attributes
    ----------
    _self_reference : `None` or ``WeakReferer`` to ``CommandProcessor``
        Reference to the command processor itself.
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
    
    _default_category_name : `str`
        The command processor's default category's name.
    
    _ignore_prefix_case : `bool`
        Whether casing in prefix is ignored.
    
    
    
    Notes
    -----
    ``CommandProcessor`` supports weakreferencing.
    """
    
    __slots__ = ('__weakref__', '_self_reference', '_precheck', '_error_handlers', '_mention_prefix_enabled',
        '_category_name_rule', '_command_name_rule', '_category_name_rule', '_command_name_rule',
        '_default_category_name', '_ignore_prefix_case')
    
    def __new__(cls, prefix, *, precheck=None, mention_prefix_enabled=True, category_name_rule=None, command_name_rule=None,
            default_category_name=None, ignore_prefix_case=True):
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
            - If `ignore_prefix_case` was not given as `bool` instance.
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
        
        if precheck is None:
            precheck = default_precheck
        else:
            test_precheck(precheck)
        
        mention_prefix_enabled = preconvert_bool(mention_prefix_enabled, 'mention_prefix_enabled')
        ignore_prefix_case = preconvert_bool(ignore_prefix_case, 'ignore_prefix_case')
        
        self = object.__new__(cls)
        self._self_reference = None
        self._precheck = precheck
        self._error_handlers = None
        self._mention_prefix_enabled = mention_prefix_enabled
        self._category_name_rule = category_name_rule
        self._command_name_rule = command_name_rule
        self._default_category_name = default_category_name
        # Assign it later, exception may occur
        self._self_reference = WeakReferer(self)
        self._ignore_prefix_case = ignore_prefix_case
        return self





