# -*- coding: utf-8 -*-

import re, reprlib

from ...backend.utils import WeakReferer

class Command:
    """
    Represents a command.
    
    Attributes
    ----------
    hidden : `bool`
        Whether the command should be hidden from help commands.
    hidden_if_checks_fail : bool`
        Whether the command should be hidden from help commands if the user's checks fail.
    aliases : `None` or `list` of `str`
        Name aliases of the command if any. They are always lower case.
    name : `str`
        The command's name.
    _category_reference : `None` or ``WeakReferer`` to ``Category``.
        Weak reference to the command's category.
    _command_processor_reference : `None` or ``WeakReferer`` to ``CommandProcessor``.
        Weak reference to the command's command processor.
    _category_hint : `str` or `None`
        Hint for the command processor to detect under which category the command should go.
    display_name : `str`
        The command's display name.
    name : `str`
        The command's name. Always lower case.
    _checks : `None` or `tuple` of ``CheckBase``
        The checks of the commands.
    """
    __slots__ = ('hidden', 'hidden_if_checks_fail', 'aliases', '_category_reference',
        '_command_processor_reference', '_category_hint', 'display_name', 'name', '_checks',)



