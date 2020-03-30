﻿# -*- coding: utf-8 -*-
__all__ = ('Category', 'CommandProcesser', 'ContentParser', 'Converter',
    'ConverterFlag', 'Cooldown', 'GUI_STATE_CANCELLED', 'GUI_STATE_CANCELLING',
    'GUI_STATE_READY', 'GUI_STATE_SWITCHING_CTX', 'GUI_STATE_SWITCHING_PAGE',
    'Pagination', 'ReactionAddWaitfor', 'ReactionDeleteWaitfor',
    'WaitAndContinue', 'checks', 'multievent', 'normalize_description',
    'prefix_by_guild', 'setup_extension', 'wait_for_message',
    'wait_for_reaction', )

import re, reprlib

from .dereaddons_local import sortedlist, modulize, MethodLike
from .futures import Task, Future

from .others import USER_MENTION_RP
from .parsers import EventWaitforBase, compare_converted, check_name,       \
    asynclist, check_argcount_and_convert, DEFAULT_EVENT

from .emoji import BUILTIN_EMOJIS
from .exceptions import DiscordException, ERROR_CODES
from .client_core import KOKORO

from .guild import Guild
from .permission import Permission
from .role import Role
from .channel import ChannelBase
from .client import Client

#Invite this as well, to shortcut imports
from .events_compiler import parse, Converter, ConverterFlag, ContentParser,\
    COMMAND_CALL_SETTING_2ARGS, COMMAND_CALL_SETTING_3ARGS, COMMAND_CALL_SETTING_USE_PARSER

COMMAND_RP=re.compile(' *([^ \t\\n]*) *(.*)')

class Command(object):
    __slots__ = ( '_call_setting', '_category_hint', '_check_failure_handler',
        '_checks', '_parser', '_parser_failure_handler', 'aliases', 'category',
        'command', 'description', 'name', )
    
    @classmethod
    def from_class(cls, klass):
        if not isinstance(klass,type):
            raise TypeError(f'Expected `type` instance, got `{klass!r}`.')
        
        name = getattr(klass,'name',None)
        if name is None:
            name = klass.__name__
        
        command = getattr(klass,'command',None)
        if command is None:
            while True:
                if type(name) is not str:
                    break
                
                command = getattr(klass,name,None)
                if (command is not None):
                    break
                
                raise ValueError('`command` class attribute is missing.')
        
        
        description = getattr(klass,'description',None)
        if description is None:
            description = klass.__doc__
        
        aliases = getattr(klass,'aliases',None)
        
        category = getattr(klass,'category',None)
        
        checks_=getattr(klass,'checks',None)
        if checks_ is None:
            checks_=getattr(klass,'checks_',None)
        
        check_failure_handler=getattr(klass,'check_failure_handler',None)
        
        parser_failure_handler=getattr(klass,'parser_failure_handler',None)
        
        return cls(command, name, description, aliases, category, checks_, check_failure_handler, parser_failure_handler)
    
    @classmethod
    def from_kwargs(cls, command, name, kwargs):
        if kwargs is None:
            description = None
            aliases = None
            category = None
            checks_ = None
            check_failure_handler = None
            parser_failure_handler = None
        else:
            description = kwargs.pop('description',None)
            aliases = kwargs.pop('aliases',None)
            category = kwargs.pop('category',None)
            checks_ = kwargs.pop('checks',None)
            check_failure_handler = kwargs.pop('check_failure_handler',None)
            parser_failure_handler = kwargs.pop('parser_failure_handler',None)
            
            if kwargs:
                raise TypeError(f'type `{cls.__name__}` not uses: `{list(kwargs)!r}`')
        
        return cls(command, name, description, aliases, category, checks_, check_failure_handler, parser_failure_handler)
    
    def __new__(cls, command, name, description, aliases, category, checks_, check_failure_handler, parser_failure_handler):
        
        name = check_name(command,name)
        
        while True:
            if aliases is None:
                aliases_processed=None
                break
            
            aliases_processed=[]
            if isinstance(aliases,str) or (not hasattr(type(aliases),'__iter__')):
                raise TypeError(f'`aliases` should have be passed as an `iterable` of `str`, got `{aliases!r}`.')
            
            for alias in aliases:
                if type(alias) is not str:
                    raise TypeError(f'`aliases` should have be passed as an `iterable` of `str`, meanwhile has at least 1 non `str` element: `{alias!r}`.')
                
                if not alias.islower():
                    alias=alias.lower()
                
                aliases_processed.append(alias)
            
            if not aliases_processed:
                aliases_processed=None
            
            aliases_processed.sort()
            
            index=len(aliases_processed)-1
            last=aliases_processed[index]
            
            while True:
                index=index-1
                if index<0:
                    break
                
                new=aliases_processed[index]
                if last==new:
                    del aliases_processed[index]
                    continue
                
                last=new
                continue
                
            if aliases_processed:
                break
            
            aliases_processed=None
            break
        
        if description is None:
            description=getattr(command,'__doc__',None)
        
        if (description is not None) and isinstance(description,str):
            description=normalize_description(description)
        
        if type(category) is Category:
            category_hint=category.name
            category=category
        elif (type(category) is str) or (category is None):
            category_hint=category
            category=None
        else:
            raise TypeError(f'`category should be type `str` or `{Category.__name__}`, got {category!r}`.')
        
        if checks_ is None:
            checks_processed=None
        else:
            checks_processed = []
            
            for check in checks_:
                if not isinstance(check, checks._check_base):
                    raise TypeError(f'`checks` should be `checks._check_base` instances, meanwhile received `{check!r}`.')
                
                checks_processed.append(check)
                continue
            
            if not checks_processed:
                checks_processed=None
        
        if check_failure_handler is None:
            if (category is not None):
                check_failure_handler = category.check_failure_handler
        else:
            check_failure_handler = check_argcount_and_convert(check_failure_handler, 5,
                '`check_failure_handler` expected 5 arguemnts (client, message, command, content, fail_identificator).')
        
        if (parser_failure_handler is not None):
            parser_failure_handler = check_argcount_and_convert(parser_failure_handler, 5,
                '`parser_failure_handler` expected 5 arguemnts (client, message, command, content, args).')
        
        if getattr(command,'__wrapper__',0):
            wrapped = True
            original = command
            while True:
                wrapper = command
                command = command.__func__
                if getattr(command,'__wrapper__',0):
                    continue
                break
        else:
            wrapped = False
        
        command, call_setting, parser = parse(command)
        
        if wrapped:
            wrapper.__func__=command
            command=original
        
        self=object.__new__(cls)
        self.command        = command
        self.name           = name
        self.aliases        = aliases_processed
        self.description    = description
        self.category       = category
        self._call_setting  = call_setting
        self._category_hint = category_hint
        self._checks        = checks_processed
        self._check_failure_handler=check_failure_handler
        self._parser        = parser
        self._parser_failure_handler=parser_failure_handler
        
        return self
    
    def __repr__(self):
        result = [
            '<',
            self.__class__.__name__,
            ' name=',
            repr(self.name),
            ', command=',
            repr(self.command),
                ]
        
        description=self.description
        if (description is not None):
            result.append(', description=')
            result.append(reprlib.repr(self.description))
        
        aliases=self.aliases
        if (aliases is not None):
            result.append(', aliases=')
            result.append(repr(aliases))
        
        checks=self._checks
        if (checks is not None):
            result.append(', checks=')
            result.append(repr(checks))
        
            check_failure_handler=self._check_failure_handler
            if (check_failure_handler is not None):
                result.append(', check_failure_handler=')
                result.append(repr(check_failure_handler))
        
        result.append(', category=')
        result.append(repr(self.category))
        
        call_setting=self._call_setting
        if call_setting != COMMAND_CALL_SETTING_2ARGS:
            if call_setting == COMMAND_CALL_SETTING_3ARGS:
                result.append(', call with content')
            else:
                result.append(', use parser')
            
            parser_failure_handler=self.parser_failure_handler
            if (parser_failure_handler is not None):
                result.append(', parser_failure_handler=')
                result.append(repr(parser_failure_handler))
            
        result.append('>')
        
        return ''.join(result)
    
    def _get_checks(self):
        checks=self._checks
        if checks is None:
            return None
        return checks.copy()
    
    def _set_checks(self,checks_):
        if checks_ is None:
            checks_processed=None
        else:
            checks_processed = []
            
            for check in checks_:
                if not isinstance(check, checks._check_base):
                    raise TypeError(f'`checks` should be `checks._check_base` instances, meanwhile received `{check!r}`.')
                
                checks_processed.append(check)
                continue
            
            if not checks_processed:
                checks_processed=None
        
        self._checks=checks_processed
    
    def _del_checks(self):
        self._checks=None
    
    checks = property(_get_checks, _set_checks, _del_checks)
    del _get_checks, _set_checks, _del_checks
    
    def _get_check_failure_handler(self):
        return self._check_failure_handler
        
    def _set_check_failure_handler(self,check_failure_handler):
        if (check_failure_handler is not None):
            check_failure_handler = check_argcount_and_convert(check_failure_handler, 5,
                '`check_failure_handler` expected 5 arguemnts (client, message, command, content, fail_identificator).')
        
        self._check_failure_handler=check_failure_handler
    
    def _del_check_failure_handler(self):
        self._check_failure_handler = self.category._check_failure_handler
    
    check_failure_handler = property(_get_check_failure_handler, _set_check_failure_handler, _del_check_failure_handler)
    del _get_check_failure_handler, _set_check_failure_handler, _del_check_failure_handler
    
    def _get_parser_failure_handler(self):
        return self._parser_failure_handler
    
    def _set_parser_failure_handler(self, parser_failure_handler):
        if parser_failure_handler is None:
            return
        
        parser_failure_handler = check_argcount_and_convert(parser_failure_handler, 5,
            '`parser_failure_handler` expected 5 arguemnts (client, message, command, content, args.')
        self._parser_failure_handler=parser_failure_handler
    
    def _del_parser_failure_handler(self):
        self._parser_failure_handler=None
    
    parser_failure_handler = property(_get_parser_failure_handler, _set_parser_failure_handler, _del_parser_failure_handler)
    del _get_parser_failure_handler, _set_parser_failure_handler, _del_parser_failure_handler
    
    @property
    def __doc__(self):
        description = self.description
        
        # go in the order of most likely cases
        if description is None:
            return None
        
        if isinstance(description,str):
            return description
        
        return None
    
    async def __call__(self, client, message, content):
        checks=self.category._checks
        if (checks is not None):
            for check in checks:
                fail_identificator = check(client, message)
                if fail_identificator==-2:
                    continue
                
                if fail_identificator==-1:
                    return 1
                
                check_failure_handler=self._check_failure_handler
                if check_failure_handler is None:
                    return 1
                
                return await check_failure_handler(client, message, self, content, fail_identificator)
        
        checks=self._checks
        if (checks is not None):
            for check in checks:
                fail_identificator = check(client, message)
                if fail_identificator==-2:
                    continue
                
                if fail_identificator==-1:
                    return 1
                
                check_failure_handler=self._check_failure_handler
                if check_failure_handler is None:
                    return 1
                
                return await check_failure_handler(client, message, self, content, fail_identificator)
        
        call_setting = self._call_setting
        if call_setting == COMMAND_CALL_SETTING_USE_PARSER:
            passed, args = await self._parser(client, message, content)
            if not passed:
                parser_failure_handler = self._parser_failure_handler
                if parser_failure_handler is None:
                    return None
                
                return await parser_failure_handler(client, message, self, content, args)
            
            return await self.command(client, message, *args)
        
        if call_setting == COMMAND_CALL_SETTING_2ARGS:
            return await self.command(client, message)
        
        # last case: COMMAND_CALL_SETTING_3ARGS
        return await self.command(client, message, content)
        
    
    async def call_checks(self, client, message, content):
        checks=self.category._checks
        if (checks is not None):
            for check in checks:
                fail_identificator = check(client, message)
                if fail_identificator==-2:
                    continue
                
                if fail_identificator==-1:
                    return 1
                
                check_failure_handler=self._check_failure_handler
                if check_failure_handler is None:
                    return 1
                
                return await check_failure_handler(client, message, self, content, fail_identificator)
        
        checks=self._checks
        if (checks is not None):
            for check in checks:
                fail_identificator = check(client, message)
                if fail_identificator==-2:
                    continue
                
                if fail_identificator==-1:
                    return 1
                
                check_failure_handler=self._check_failure_handler
                if check_failure_handler is None:
                    return 1
                
                return await check_failure_handler(client, message, self, content, fail_identificator)
    
    def run_all_checks(self, client, message):
        checks=self.category._checks
        if (checks is not None):
            for check in checks:
                fail_identificator = check(client, message)
                if fail_identificator==-2:
                    continue
                
                return False
        
        checks=self._checks
        if (checks is not None):
            for check in checks:
                fail_identificator = check(client, message)
                if fail_identificator==-2:
                    continue
                
                return False
        
        return True
    
    def run_checks(self, client, message):
        checks=self._checks
        if (checks is not None):
            for check in checks:
                fail_identificator = check(client, message)
                if fail_identificator==-2:
                    continue
                
                return False
        
        return True
    
    async def call_command(self, client, message, content):
        call_setting = self._call_setting
        if call_setting == COMMAND_CALL_SETTING_USE_PARSER:
            passed, args = await self._parser(client, message, content)
            if not passed:
                parser_failure_handler = self._parser_failure_handler
                if parser_failure_handler is None:
                    return None
                
                return await parser_failure_handler(client, message, self, content, args)
            
            return await self.command(client, message, *args)
        
        if call_setting == COMMAND_CALL_SETTING_2ARGS:
            return await self.command(client, message)
        
        # last case: COMMAND_CALL_SETTING_3ARGS
        return await self.command(client, message, content)
    
    def __getattr__(self,name):
        return getattr(self.command,name)
    
    def __gt__(self,other):
        return self.name>other.name
    
    def __ge__(self,other):
        return self.name>=other.name
    
    def __eq__(self,other):
        return self.name==other.name
    
    def __ne__(self,other):
        return self.name!=other.name
    
    def __le__(self,other):
        return self.name<=other.name
    
    def __lt__(self,other):
        return self.name<other.name

def normalize_description(text):
    lines=text.splitlines()
    
    for index in range(len(lines)):
        lines[index]=lines[index].rstrip()
    
    while True:
        if not lines:
            return None
        
        line=lines[0]
        if line:
            break
        
        del lines[0]
        continue
    
    while True:
        if not lines:
            return None
        
        line=lines[-1]
        if line:
            break
        
        del lines[-1]
        continue
    
    limit=len(lines)
    if limit==1:
        return lines[0].lstrip()
    
    ignore_index=0
    
    while True:
        next_char=lines[0][ignore_index]
        if next_char not in ('\t', ' '):
            break
        
        index=1
        while index<limit:
            line=lines[index]
            index=index+1
            if not line:
                continue
            
            char=line[ignore_index]
            if char!=next_char:
                break
            
            continue
        
        if char!=next_char:
            break
        
        ignore_index=ignore_index+1
        continue
    
    if ignore_index!=0:
        for index in range(len(lines)):
            line=lines[index]
            if not line:
                continue
            
            lines[index]=line[ignore_index:]
            continue
    
    return '\n'.join(lines)

@modulize
class checks:
    def _convert_fail_identificator(fail_identificator):
        if fail_identificator is None:
            return 1
        
        if not isinstance(fail_identificator,int):
            raise TypeError(f'`fail_identificator` should have been passed as `int` instance, got `{fail_identificator!r}`')
        
        if type(fail_identificator) is not int:
            fail_identificator=int(fail_identificator)
        
        if fail_identificator<0:
            raise ValueError(f'`fail_identificator` value was passed as a negative number: `{fail_identificator!r}`.')
        
        return fail_identificator
    
    def _convert_permissions(permissions):
        if type(permissions) is Permission:
            return permissions
        
        if isinstance(permissions,int):
            return Permission(permissions)
        
        raise TypeError(f'`permissions` should have been passed as a `Permission` object or as an `int` instance, got `{permissions!r}`.')
    
    def _convert_guild(guild):
        if type(guild) is Guild:
            return guild.id
        
        if isinstance(guild,int):
            if type(guild) is not int:
                guild=int(guild)
            
            return guild
        
        raise TypeError(f'`guild` should have been passed as a `Guild` object or as an `int` instance, got `{guild!r}`.')
    
    def _convert_role(role):
        if type(role) is Role:
            return role
        
        if isinstance(role,int):
            if type(role) is not int:
                role=int(role)
            
            return Role.precreate(role)
        
        raise TypeError(f'`role` should have been passed as a `Role` object or as an `int` instance, got `{role!r}`.')
    
    def _convert_channel(channel):
        if isinstance(channel,ChannelBase):
            return channel.id
        
        if isinstance(channel,int):
            if type(channel) is not int:
                channel=int(channel)
            
            return channel
        
        raise TypeError(f'`channel` should have been passed as a `ChannelBase` or as `int` instance, got `{channel!r}`.')
    
    class _check_base(object):
        __slots__ = ('fail_identificator',)
        def __init__(self, fail_identificator=None):
            self.fail_identificator = checks._convert_fail_identificator(fail_identificator)
        
        def __call__(self, client, message):
            return self.fail_identificator
        
        def __repr__(self):
            result = [
                self.__class__.__name__,
                '(',
                    ]
            
            slots=self.__slots__
            limit=len(slots)
            if limit:
                index=0
                while True:
                    name=slots[index]
                    index=index+1
                    
                    result.append(name)
                    result.append('=')
                    attr=getattr(self,name)
                    result.append(repr(attr))
                    
                    if index==limit:
                        break
                    
                    result.append(', ')
                    continue
            
            fail_identificator = self.fail_identificator
            
            if fail_identificator!=1:
                if limit:
                    result.append(', ')
                result.append('fail_identificator=')
                result.append(repr(fail_identificator))
            
            result.append(')')
            
            return ''.join(result)
    
    class has_role(_check_base):
        __slots__ = ('role', )
        def __init__(self, role, fail_identificator=None):
            self.role = checks._convert_role(role)
            self.fail_identificator = checks._convert_fail_identificator(fail_identificator)
        
        def __call__(self, client, message):
            if message.author.has_role(self.role):
                return -2
            
            return self.fail_identificator
    
    class owner_or_has_role(has_role):
        def __call__(self, client, message):
            user=message.author
            if user.has_role(self.role):
                return -2
            
            if client.is_owner(user):
                return -2
            
            return self.fail_identificator
    
    class has_any_role(_check_base):
        __slots__ = ('roles', )
        def __init__(self, roles, fail_identificator=None):
            roles_processed = set()
            for role in roles:
                role = checks._convert_role(role)
                roles_processed.add(role)
            
            self.roles = roles_processed
            self.fail_identificator = checks._convert_fail_identificator(fail_identificator)
        
        def __call__(self, client, message):
            user=message.author
            if user.has_role(self.roles):
                return -2
            
            return self.fail_identificator
    
    class owner_or_has_any_role(has_any_role):
        def __call__(self, client, message):
            user=message.author
            for role in self.roles:
                if user.has_role(role):
                    return -2
            
            if client.is_owner(user):
                return -2
            
            return self.fail_identificator
    
    class guild_only(_check_base):
        __slots__ = ()
        
        def __call__(self, client, message):
            if (message.guild is not None):
                return -2
            
            return self.fail_identificator
    
    class private_only(_check_base):
        __slots__ = ()
        def __call__(self, client, message):
            if (message.guild is None):
                return -2
            
            return self.fail_identificator
    
    class owner_only(_check_base):
        __slots__ = ()
        def __call__(self, client, message):
            if client.is_owner(message.author):
                return -2
            
            return self.fail_identificator
    
    class guild_owner(_check_base):
        __slots__ = ()
        def __call__(self, client, message):
            guild = message.channel.guild
            if guild is None:
                return self.fail_identificator
            
            if guild.owner==message.author:
                return -2
            
            return self.fail_identificator
    
    class owner_or_guild_owner(guild_owner):
        __slots__ = ()
        def __call__(self, client, message):
            guild = message.channel.guild
            if guild is None:
                return self.fail_identificator
            
            user = message.author
            if guild.owner==user:
                return -2
            
            if client.is_owner(user):
                return -2
            
            return self.fail_identificator
    
    class has_permissions(_check_base):
        __slots__ = ('permissions', )
        def __init__(self, permissions, fail_identificator=None):
            permissions = checks._convert_permissions(permissions)
            fail_identificator = checks._convert_fail_identificator(fail_identificator)
            
            self.permissions = permissions
            self.fail_identificator = fail_identificator
        
        def __call__(self, client, message):
            if message.channel.permissions_for(message.author)>=self.permissions:
                return -2
            
            return self.fail_identificator
    
    class owner_or_has_permissions(has_permissions):
        def __call__(self, client, message):
            user=message.author
            if message.channel.permissions_for(user)>=self.permissions:
                return -2
            
            if client.is_owner(user):
                return -2
            
            return self.fail_identificator
    
    class has_guild_permissions(_check_base):
        __slots__ = ('permissions', )
        def __init__(self, permissions, fail_identificator=None):
            permissions = checks._convert_permissions(permissions)
            fail_identificator = checks._convert_fail_identificator(fail_identificator)
            
            self.permissions = permissions
            self.fail_identificator = fail_identificator
        
        def __call__(self, client, message):
            guild = message.channel.guild
            if guild is None:
                return self.fail_identificator
            
            if guild.permissions_for(message.author)>=self.permissions:
                return -2
            
            return self.fail_identificator
    
    class owner_or_has_guild_permissions(has_permissions):
        __slots__ = ('permissions', )
        def __call__(self, client, message):
            guild = message.channel.guild
            if guild is None:
                return self.fail_identificator
            
            if guild.permissions_for(message.author)>=self.permissions:
                return 0
            
            return self.fail_identificator
            
            if client.is_owner(user):
                return -2
            
            return self.fail_identificator
    
    class client_has_permissions(_check_base):
        __slots__ = ('permissions', )
        def __init__(self, permissions, fail_identificator=None):
            permissions = checks._convert_permissions(permissions)
            fail_identificator = checks._convert_fail_identificator(fail_identificator)
            
            self.permissions = permissions
            self.fail_identificator = fail_identificator
        
        def __call__(self, client, message):
            if message.channel.cached_permissions_for(client)>=self.permissions:
                return -2
            
            return self.fail_identificator
    
    class client_has_guild_permissions(_check_base):
        __slots__ = ('permissions', )
        def __init__(self, permissions, fail_identificator=None):
            permissions = checks._convert_permissions(permissions)
            fail_identificator = checks._convert_fail_identificator(fail_identificator)
            
            self.permissions = permissions
            self.fail_identificator = fail_identificator
        
        def __call__(self, client, message):
            guild = message.channel.guild
            if guild is None:
                return self.fail_identificator
            
            if guild.cached_permissions_for(client)>=self.permissions:
                return -2
            
            return self.fail_identificator
    
    class is_guild(_check_base):
        __slots__ = ('guild_id', )
        def __init__(self, guild_id, fail_identificator=None):
            guild_id = checks._covert_guild(guild_id)
            fail_identificator = checks._convert_fail_identificator(fail_identificator)
            
            self.guild_id = guild_id
            self.fail_identificator = fail_identificator
        
        def __call__(self, client, message):
            guild = message.channel.guild
            if guild is None:
                return self.fail_identificator
            
            if (guild.id==self.guild_id):
                return -2
            
            return self.fail_identificator
        
    class is_any_guild(_check_base):
        __slots__ = ('guild_ids', )
        def __init__(self, guild_ids, fail_identificator=None):
            guild_ids_processed = set()
            for guild in guild_ids:
                guild_id = checks._covert_guild(guild)
                guild_ids.add(guild_id)
            
            fail_identificator = checks._convert_fail_identificator(fail_identificator)
            
            self.guild_ids = guild_ids_processed
            self.fail_identificator = fail_identificator
        
        def __call__(self, client, message):
            guild = message.channel.guild
            if guild is None:
                return self.fail_identificator
            
            if (guild.id in self.guild_ids):
                return -2
            
            return self.fail_identificator
        
    class custom(_check_base):
        __slots__ = ('function', )
        def __init__(self, function, fail_identificator=None):
            function = check_argcount_and_convert(function, 2)
            fail_identificator = checks._convert_fail_identificator(fail_identificator)
            
            self.function = function
            self.fail_identificator = fail_identificator
        
        def __call__(self, client, message):
            try:
                result = self.function(client, message)
            except BaseException as err:
                Task(client.events.error(client,repr(self),err),client.loop)
                return self.fail_identificator
            
            if result is None:
                return self.fail_identificator
            
            if isinstance(result,int) and result:
                return -2
            
            return self.fail_identificator
    
    class is_channel(_check_base):
        __slots__ = ('channel_id', )
        def __init__(self, channel, fail_identificator=None):
            channel_id = checks._covert_guild(channel)
            fail_identificator = checks._convert_fail_identificator(fail_identificator)
            
            self.channel_id = channel_id
            self.fail_identificator = fail_identificator
        
        def __call__(self, client, message):
            if (message.channel.id==self.channel_id):
                return -2
            
            return self.fail_identificator
        
    class is_any_channel(_check_base):
        __slots__ = ('channel_ids', )
        def __init__(self, channels, fail_identificator=None):
            channel_ids = set()
            for channel in channels:
                channel_id = checks._covert_guild(channel)
                channel_ids.add(channel_id)
            
            fail_identificator = checks._convert_fail_identificator(fail_identificator)
            
            self.channel_ids = channel_ids
            self.fail_identificator = fail_identificator
        
        def __call__(self, client, message):
            if (message.channel.id in self.channel_ids):
                return -2
            
            return self.fail_identificator

class Category(object):
    __slots__ = ('_checks', '_check_failure_handler', 'commands', 'description', 'name', )
    def __new__(cls, name, checks_ = None, check_failure_handler=None, description=None):
        
        if checks_ is None:
            checks_processed=None
        else:
            checks_processed = []
            for check in checks_:
                if not isinstance(check, checks._check_base):
                    raise TypeError(f'`checks` should be `checks._check_base` instances, meanwhile received `{check!r}`.')
                
                checks_processed.append(check)
                continue
            
            if not checks_processed:
                checks_processed=None
        
        if (check_failure_handler is not None):
            check_failure_handler = check_argcount_and_convert(check_failure_handler, 5,
                '`check_failure_handler` expected 5 arguemnts (client, message, command, content, fail_identificator).')
        
        if (description is not None) and isinstance(description,str):
            description=normalize_description(description)
        
        self=object.__new__(cls)
        self.name=name
        self.commands=sortedlist()
        self._checks = checks_processed
        self._check_failure_handler = check_failure_handler
        self.description=description
        return self
    
    def _get_checks(self):
        checks=self._checks
        if checks is None:
            return None
        return checks.copy()
    
    def _set_checks(self, checks_):
        if checks_ is None:
            checks_processed=None
        else:
            checks_processed = []
            for check in checks_:
                if not isinstance(check, checks._check_base):
                    raise TypeError(f'`checks` should be `checks._check_base` instances, meanwhile received `{check!r}`.')
                
                checks_processed.append(check)
                continue
            
            if not checks_processed:
                checks_processed=None
            
        self._checks=checks_processed
    
    def _del_checks(self):
        self._checks=None
    
    checks=property(_get_checks,_set_checks, _del_checks)
    del _get_checks, _set_checks, _del_checks
    
    def _get_check_failure_handler(self):
        return self._check_failure_handler
    
    def _set_check_failure_handler(self, check_failure_handler):
        if (check_failure_handler is not None):
            check_failure_handler = check_argcount_and_convert(check_failure_handler, 5,
                '`check_failure_handler` expected 5 arguemnts (client, message, command, content, fail_identificator).')
        
        actual_check_failure_handler=self._check_failure_handler
        self._check_failure_handler=check_failure_handler
        
        for command in self.commands:
            if command._check_failure_handler is actual_check_failure_handler:
                command._check_failure_handler=check_failure_handler
    
    def _del_check_failure_handler(self):
        actual_check_failure_handler=self._check_failure_handler
        if actual_check_failure_handler is None:
            return
        
        self._check_failure_handler=None
        
        for command in self.commands:
            if command._check_failure_handler is actual_check_failure_handler:
                command._check_failure_handler=None
    
    check_failure_handler=property(_get_check_failure_handler,_set_check_failure_handler, _del_check_failure_handler)
    del _get_check_failure_handler, _set_check_failure_handler, _del_check_failure_handler
    
    def run_checks(self, client, message):
        checks=self._checks
        if (checks is not None):
            for check in checks:
                fail_identificator = check(client, message)
                if fail_identificator==-2:
                    continue
                
                return False
        
        return True
    
    def __gt__(self,other):
        self_name=self.name
        other_name=other.name
        
        if self_name is None:
##            if other_name is None:
##                return False
##            else:
##                return False
            return False
        else:
            if other_name is None:
                return True
            else:
                return (self_name>other_name)
    
    def __ge__(self,other):
        self_name=self.name
        other_name=other.name
        
        if self_name is None:
            if other_name is None:
                return True
            else:
                return False
        else:
            if other_name is None:
                return True
            else:
                return (self_name>=other_name)
    
    def __eq__(self,other):
        self_name=self.name
        other_name=other.name
        
        if self_name is None:
            if other_name is None:
                return True
            else:
                return False
        else:
            if other_name is None:
                return False
            else:
                return (self_name==other_name)
    
    def __ne__(self,other):
        self_name=self.name
        other_name=other.name
        
        if self_name is None:
            if other_name is None:
                return False
            else:
                return True
        else:
            if other_name is None:
                return True
            else:
                return (self_name!=other_name)
    
    def __le__(self,other):
        self_name=self.name
        other_name=other.name
        
        if self_name is None:
##            if other_name is None:
##                return True
##            else:
##                return True
            return True
        else:
            if other_name is None:
                return False
            else:
                return (self_name<=other_name)
    
    def __lt__(self,other):
        self_name=self.name
        other_name=other.name
        
        if self_name is None:
            if other_name is None:
                return False
            else:
                return True
        else:
            if other_name is None:
                return False
            else:
                return (self_name<=other_name)
    
    def __iter__(self):
        return iter(self.commands)
    
    def __reversed__(self):
        return reversed(self.commands)
    
    def __len__(self):
        return len(self.commands)
    
    def __repr__(self):
        result = [
            '<',
            self.__class__.__name__,
                ]
        name=self.name
        if (name is not None):
            result.append(' ')
            result.append(name)
            
        result.append(' length=')
        result.append(repr(len(self.commands)))
        result.append(', checks=')
        result.append(repr(self._checks))
        result.append(', check_failure_handler=')
        result.append(repr(self.check_failure_handler))
        result.append('>')
        
        return ''.join(result)

class CommandProcesser(EventWaitforBase):
    __slots__ = ('_default_category_name', '_ignorecase', 'categories',
        'command_error', 'commands', 'default_event', 'invalid_command',
        'mention_prefix', 'prefix', 'prefixfilter', )
    
    __event_name__='message_create'
    
    SUPPORTED_TYPES = (Command, )
    
    def __new__(cls, prefix, ignorecase=True, mention_prefix=True, default_category_name=None):
        if (default_category_name is not None):
            if not isinstance(default_category_name,str):
                raise TypeError(f'`default_category_name` should have been passed as `None`, or as `str` instance, meanwhile got `{default_category_name!r}`.')
        
            if not default_category_name:
                default_category_name=None
        
        self = object.__new__(cls)
        self.command_error=DEFAULT_EVENT
        self.default_event=DEFAULT_EVENT
        self.invalid_command=DEFAULT_EVENT
        self.mention_prefix=mention_prefix
        self.commands={}
        self.update_prefix(prefix,ignorecase)
        self._ignorecase=ignorecase
        
        self._default_category_name=default_category_name
        categories=sortedlist()
        self.categories=categories
        categories.add(Category(default_category_name))
        return self
    
    def get_category(self, category_name):
        # category name can be None, but when we wanna use `.get` we need to
        # use compareable datatypes, so whenever we get we need to convert
        # `None` to empty `str` at every case
        if category_name is None:
            category_name=self._default_category_name
            if category_name is None:
                category_name = ''
        
        elif not isinstance(category_name,str):
            raise TypeError(f'The passed `{category_name!r}` should have been passed as`None` as `str` instance.')
        
        elif not category_name:
            category_name=self._default_category_name
            if category_name is None:
                category_name = ''
        
        return self.categories.get(category_name, key=self._get_category_key)
    
    def get_default_category(self):
        category_name = self._default_category_name
        if category_name is None:
            category_name = ''
        return self.categories.get(category_name, key=self._get_category_key)
    
    @staticmethod
    def _get_category_key(category):
        name=category.name
        if name is None:
            return ''
        
        return name
    
    def _get_default_category_name(self):
        return self._default_category_name
    
    def _set_default_category_name(self, value):
        if (value is not None):
            if not isinstance(value,str):
                raise TypeError(f'Category name can be `None` or `str` instance, got `{value!r}`.')
            
            if not value:
                value=None
        
        # if both is same, dont do anything
        default_category_name = self._default_category_name
        if value is None:
            if default_category_name is None:
                return
        else:
            if (default_category_name is not None) and (value==default_category_name):
                return
        
        other_category = self.get_category(value)
        if (other_category is not None):
            raise ValueError(f'There is already a category added with that name: `{value!r}`')
        
        default_category = self.get_category(default_category_name)
        default_category.name = value
        self.categories.resort()
        self._default_category_name = value
    
    default_category_name = property(_get_default_category_name,_set_default_category_name)
    del _get_default_category_name, _set_default_category_name
    
    def create_category(self, name, checks=None, check_failure_handler=None, description=None):
        category=self.get_category(name)
        if (category is not None):
            raise ValueError(f'There is already a category added with that name: `{name!r}`')
        
        category=Category(name,checks,check_failure_handler,description)
        self.categories.add(category)
        return category
    
    def delete_category(self, category):
        if isinstance(category,str):
            if (not category):
                raise ValueError('Default category cannot be deleted.')
            default_category_name=self._default_category_name
            if (default_category_name is not None) and (category==default_category_name):
                raise ValueError('Default category cannot be deleted.')
            category_name = category
        elif type(category) is Category:
            category_name = category.name
        elif category is None:
            raise ValueError('Default category cannot be deleted.')
        else:
            raise TypeError(f'Expected type `str` instance or `{Category.__name__}`, got `{category!r}`.')
        
        category = self.categories.pop(category_name, key=self._get_category_key)
        if category is None:
            return
        
        commands=self.commands
        for command in category.commands:
            name=command.name
            other_command=commands.get(name)
            if other_command is command:
                del commands[name]
            
            aliases=command.aliases
            if aliases is None:
                continue
            
            for name in aliases:
                other_command=commands.get(name)
                if other_command is command:
                    del commands[name]
    
    def update_prefix(self,prefix,ignorecase=None):
        if ignorecase is None:
            ignorecase=self._ignorecase
        if ignorecase:
            flag=re.I
        else:
            flag=0
        
        while True:
            if callable(prefix):
                def prefixfilter(message):
                    practical_prefix=prefix(message)
                    if re.match(re.escape(practical_prefix),message.content,flag) is None:
                        return
                    result=COMMAND_RP.match(message.content,len(practical_prefix))
                    if result is None:
                        return
                    return result.groups()
                
                break
            
            if type(prefix) is str:
                PREFIX_RP=re.compile(re.escape(prefix),flag)
            elif isinstance(prefix,(list,tuple)):
                PREFIX_RP=re.compile("|".join(re.escape(p) for p in prefix),flag)
            else:
                raise TypeError(f'Prefix can be only callable, str or tuple/list type, got {prefix!r}')
            
            def prefixfilter(message):
                result=PREFIX_RP.match(message.content)
                if result is None:
                    return
                result=COMMAND_RP.match(message.content,result.end())
                if result is None:
                    return
                return result.groups()
            
            break
        
        self.prefix=prefix
        self.prefixfilter=prefixfilter
        self._ignorecase=ignorecase
    
    def __setevent__(self, func, name, description=None, aliases=None, category=None, checks=None, check_failure_handler=None, parser_failure_handler=None):
        
        if type(func) is Command:
            return self._add_command(func)
        
        # called every time, but only if every other fails
        if name=='default_event':
            func=check_argcount_and_convert(func, 2, '`default_event` expects 2 arguments (client, message).')
            self.default_event=func
            return func
        
        # called when user used bad command after the preset prefix, called if a command fails
        if name=='invalid_command':
            func=check_argcount_and_convert(func, 4, '`invalid_command` expected 4 arguemnts (client, message, command, content).')
            self.invalid_command=func
            return func
        
        if name=='command_error':
            func=check_argcount_and_convert(func, 5, '`invalid_command` expected 5 arguemnts (client, message, command, content, exception).')
            self.command_error=func
            return func
        
        # called first
        
        command=Command(func, name, description, aliases, category, checks, check_failure_handler, parser_failure_handler)
        return self._add_command(command)
        
    def __setevent_from_class__(self, klass):
        command = Command.from_class(klass)
        return self._add_command(command)
    
    def _add_command(self, command):
        category=command.category
        if (category is not None):
            if self.get_category(category.name) is not category:
                raise ValueError(f'The passed `{Category.__class__.__name__}` object is not owned; `{category!r}`.')
            category_added=True
        
        else:
            category_hint = command._category_hint
            if category_hint is None:
                category_hint=self._default_category_name
            
            category=self.get_category(category_hint)
            if category is None:
                category=Category(category_hint)
                category_added=False
            else:
                category_added=True
            
            command.category = category
        
        commands=self.commands
        name=command.name
        
        would_overwrite=commands.get(name)
        if (would_overwrite is not None) and (would_overwrite.name!=name):
            raise ValueError(f'The command would overwrite an alias of an another one: `{would_overwrite}`.'
                'If you intend to overwrite an another command please overwrite it with it\'s default name.')
        
        aliases=command.aliases
        if (aliases is not None):
            for alias in aliases:
                try:
                    overwrites=commands[alias]
                except KeyError:
                    continue
                
                if overwrites is would_overwrite:
                    continue
                
                error_message_parts = [
                    'Alias `',
                    repr(alias),
                    '` would overwrite an other command; `',
                    repr(overwrites),
                    '`.'
                        ]
                
                if (would_overwrite is not None):
                    error_message_parts.append(' The command already overwrites an another one with the same name: `')
                    error_message_parts.append(repr(would_overwrite))
                    error_message_parts.append('`.')
                
                raise ValueError(''.join(error_message_parts))
        
        if (would_overwrite is not None):
            aliases=would_overwrite.aliases
            if (aliases is not None):
                for alias in aliases:
                    if commands[alias] is would_overwrite:
                        del commands[alias]
            
            category=would_overwrite.category
            if (category is not None):
                category.commands.remove(would_overwrite)
            
        # If everything is correct check for category, create it if needed,
        # add to it. Then add to the commands as well with it's aliases ofc.
        
        category.commands.add(command)
        if not category_added:
            self.categories.add(category)
        commands[name]=command
        
        aliases=command.aliases
        if (aliases is not None):
            for alias in aliases:
                commands[alias]=command
        
        return command
    
    def __delevent__(self, func, name, **kwargs):
        if (name is not None) and (not type(name) is str):
            raise TypeError(f'Case should have been `str`, or can be `None` if `func` is passed as `Command` instance. Got `{name!r}`.')
        
        if type(func) is Command:
            commands=self.commands
            if (name is None) or (name==func.name):
                found_names=[]
                
                name=func.name
                try:
                    command=commands[name]
                except KeyError:
                    pass
                else:
                    if command is func:
                        found_names.append(name)
                
                aliases=func.aliases
                if (aliases is not None):
                    for name in aliases:
                        try:
                            command=commands[name]
                        except KeyError:
                            pass
                        else:
                            if command is func:
                                found_names.append(name)
                
                if not found_names:
                    raise ValueError(f'The passed command `{func!r}` is not added with any of it\'s own names as a command.')
                
                for name in found_names:
                    del commands[name]
                    
                category=self.get_category(func.name)
                if (category is not None):
                    category.commands.remove(func)
                
                return
            
            aliases=func.aliases
            if (aliases is None):
                raise ValueError(f'The passed name `{name!r}` is not the name, neither an alias of the command `{func!r}`')
            
            try:
                position=aliases.index(name)
            except ValueError:
                raise ValueError(f'The passed name `{name!r}` is not the name, neither an alias of the command `{func!r}`')
            
            try:
                command=commands[name]
            except KeyError:
                raise ValueError(f'At the passed name `{name!r}` there is no command removed, so it cannot be deleted either.')
            
            if func is not command:
                raise ValueError(f'At the specified name `{name!r}` there is a different command added already.')
            
            del aliases[position]
            if not aliases:
                func.aliases=None
            
            del commands[name]
            return
            
        if name is None:
            raise TypeError(f'Case should have been passed as `str`, if `func` is not passed as `Command` instance, `{func!r}`.')
        
        if name=='default_event':
            if func is self.default_event:
                self.default_event=DEFAULT_EVENT
                return
            
            raise ValueError(f'The passed `{name!r}` ({func!r}) is not the same as the already loaded one: `{self.default_event!r}`')
        
        if name=='invalid_command':
            if func is self.invalid_command:
                self.invalid_command=DEFAULT_EVENT
                return
            
            raise ValueError(f'The passed `{name!r}` ({func!r}) is not the same as the already loaded one: `{self.invalid_command!r}`')
        
        if name=='command_error':
            if func is self.command_error:
                self.command_error=DEFAULT_EVENT
                return
            
            raise ValueError(f'The passed `{name!r}` ({func!r}) is not the same as the already loaded one: `{self.command_error!r}`')
        
        try:
            command=self.commands[name]
        except KeyError:
            raise ValueError(f'The passed `{name!r}` is not added as a command right now.') from None
        
        if compare_converted(command.command,func):
            del self.commands[name]
            return
        
        raise ValueError(f'The passed `{name!r}` (`{func!r}`) command is not the same as the already loaded one: `{command!r}`')
    
    async def __call__(self,client,message):
        await self.call_waitfors(client, message)
        
        if message.author.is_bot:
            return
        
        if not message.channel.cached_permissions_for(client).can_send_messages:
            return
        
        result=self.prefixfilter(message)
        
        if result is None:
            #start goto if needed
            while self.mention_prefix and (message.mentions is not None) and (client in message.mentions):
                result=USER_MENTION_RP.match(message.content)
                if result is None or int(result.group(1))!=client.id:
                    break
                result=COMMAND_RP.match(message.content,result.end())
                if result is None:
                    break
                
                command_name,content=result.groups()
                command_name=command_name.lower()
                
                try:
                    command=self.commands[command_name]
                except KeyError:
                    break
                
                try:
                    result = await command(client,message,content)
                except BaseException as err1:
                    command_error=self.command_error
                    if command_error is not DEFAULT_EVENT:
                        try:
                            result = await command_error(client,message,command_name,content,err1)
                        except BaseException as err2:
                            await client.events.error(client,repr(self),err2)
                            return
                        else:
                            if result is None:
                                return
                            elif not isinstance(result,int):
                                return
                            elif not result:
                                return
                    
                    await client.events.error(client,repr(self),err1)
                    return
                
                else:
                    if not result:
                        return
        
        else:
            command_name,content=result
            command_name=command_name.lower()
            
            try:
                command=self.commands[command_name]
            except KeyError:
                await self.invalid_command(client,message,command_name,content)
                return
            
            try:
                result = await command(client,message,content)
            except BaseException as err1:
                command_error=self.command_error
                if command_error is not DEFAULT_EVENT:
                    try:
                        result = await command_error(client,message,command_name,content,err1)
                    except BaseException as err2:
                        await client.events.error(client,repr(self),err2)
                        return
                    else:
                        if result is None:
                            return
                        elif not isinstance(result,int):
                            return
                        elif not result:
                            return
                
                await client.events.error(client,repr(self),err1)
                return
            
            else:
                if result is None:
                    return
                elif not isinstance(result,int):
                    return
                elif not result:
                    return
                
                await self.invalid_command(client,message,command_name,content)
                return
            
            return
        
        await self.default_event(client,message)
        return
    
    def __repr__(self):
        result = [
            '<', self.__class__.__name__,
            ' prefix=', repr(self.prefix),
            ', command count=', repr(self.command_count),
            ', mention_prefix=', repr(self.mention_prefix),
                ]
        
        default_event=self.default_event
        if default_event is not DEFAULT_EVENT:
            result.append(', default_event=')
            result.append(repr(default_event))
        
        invalid_command=self.invalid_command
        if invalid_command is not DEFAULT_EVENT:
            result.append(', invalid_command=')
            result.append(repr(invalid_command))
        
        command_error=self.command_error
        if command_error is not DEFAULT_EVENT:
            result.append(', command_error=')
            result.append(repr(command_error))
        
        result.append('>')
        
        return ''.join(result)
    
    @property
    def command_count(self):
        count=0
        for category in self.categories:
            count+=len(category.commands)
        
        return count

class ReactionAddWaitfor(EventWaitforBase):
    __slots__ = ()
    __event_name__ = 'reaction_add'

class ReactionDeleteWaitfor(EventWaitforBase):
    __slots__ = ()
    __event_name__ = 'reaction_delete'

class multievent(object):
    __slots__=('events',)
    
    def __init__(self,*events):
        self.events=events
    
    def append(self, target, waiter):
        for event in self.events:
            event.append(target, waiter)
    
    def remove(self, target, waiter):
        for event in self.events:
            event.remove(target, waiter)

class Timeouter(object):
    __slots__=('loop', 'handler', 'owner', 'timeout')
    def __init__(self,loop,owner,timeout):
        self.loop=loop
        self.owner=owner
        self.timeout=timeout
        self.handler=loop.call_later(timeout,self.__step,self)
    
    @staticmethod
    def __step(self):
        timeout=self.timeout
        if timeout>0.0:
            self.handler=self.loop.call_later(timeout,self.__step,self)
            self.timeout=0.0
            return
        
        self.handler=None
        owner=self.owner
        if owner is None:
            return
        
        self.owner=None
        
        canceller=owner.canceller
        if canceller is None:
            return
        owner.canceller=None
        Task(canceller(owner,TimeoutError()),self.loop)
        
        
    def cancel(self):
        handler=self.handler
        if handler is None:
            return
        
        self.handler=None
        handler.cancel()
        self.owner=None
    
    def set_timeout(self,value):
        handler=self.handler
        if handler is None:
            # Cannot change timeout of expired timeouter
            return
        
        if value<=0.0:
            self.timeout=0.0
            handler._run()
            handler.cancel()
            return
        
        now=self.loop.time()
        next_step=self.handler.when
        
        planed_end=now+value
        if planed_end<next_step:
            handler.cancel()
            self.handler=self.loop.call_at(planed_end,self.__step,self)
            return
        
        self.timeout=planed_end-next_step
        
    def get_expiration_delay(self):
        return self.handler.when-self.loop.time()+self.timeout
        
GUI_STATE_READY          = 0
GUI_STATE_SWITCHING_PAGE = 1
GUI_STATE_CANCELLING     = 2
GUI_STATE_CANCELLED      = 3
GUI_STATE_SWITCHING_CTX  = 4

class Pagination(object):
    LEFT2   = BUILTIN_EMOJIS['track_previous']
    LEFT    = BUILTIN_EMOJIS['arrow_backward']
    RIGHT   = BUILTIN_EMOJIS['arrow_forward']
    RIGHT2  = BUILTIN_EMOJIS['track_next']
    CANCEL  = BUILTIN_EMOJIS['x']
    EMOJIS  = (LEFT2,LEFT,RIGHT,RIGHT2,CANCEL,)
    
    __slots__=('canceller', 'channel', 'client', 'message', 'page', 'pages',
        'task_flag', 'timeout', 'timeouter')
    
    async def __new__(cls,client,channel,pages,timeout=240.,message=None):
        self=object.__new__(cls)
        self.client=client
        self.channel=channel
        self.pages=pages
        self.page=0
        self.canceller=cls._canceller
        self.task_flag=GUI_STATE_READY
        self.message=message
        self.timeout=timeout
        self.timeouter=None
        
        if message is None:
            message = await client.message_create(channel,embed=pages[0])
            self.message=message
        
        if not channel.cached_permissions_for(client).can_add_reactions:
            return self
        
        if len(self.pages)>1:
            for emoji in self.EMOJIS:
                await client.reaction_add(message,emoji)
        else:
            await client.reaction_add(message,self.CANCEL)
        
        self.timeouter=Timeouter(client.loop,self,timeout=timeout)
        client.events.reaction_add.append(message, self)
        client.events.reaction_delete.append(message, self)
        return self
    
    async def __call__(self, client, message, emoji, user):
        if user.is_bot or (emoji not in self.EMOJIS):
            return
        
        if self.channel.cached_permissions_for(client).can_manage_messages:
            if not message.did_react(emoji,user):
                return
            
            Task(self._reaction_delete(emoji,user),client.loop)
        
        task_flag=self.task_flag
        if task_flag!=GUI_STATE_READY:
            if task_flag==GUI_STATE_SWITCHING_PAGE:
                if emoji is self.CANCEL:
                    self.task_flag=GUI_STATE_CANCELLING
                return
            
            # ignore GUI_STATE_CANCELLED and GUI_STATE_SWITCHING_CTX
            return
        
        while True:
            if emoji is self.LEFT:
                page=self.page-1
                break
            
            if emoji is self.RIGHT:
                page=self.page+1
                break
            
            if emoji is self.CANCEL:
                self.task_flag=GUI_STATE_CANCELLED
                try:
                    await client.message_delete(message)
                except BaseException as err:
                    self.cancel()
                    
                    if isinstance(err,ConnectionError):
                        # no internet
                        return
                    
                    if isinstance(err,DiscordException):
                        if err.code in (
                                ERROR_CODES.unknown_channel, # message's channel deleted
                                ERROR_CODES.missing_access, # client removed
                                    ):
                            return
                    
                    await client.events.error(client,f'{self!r}.__call__',err)
                    return
                
                else:
                    self.cancel()
                    return
            
            if emoji is self.LEFT2:
                page=0
                break
            
            if emoji is self.RIGHT2:
                page=len(self.pages)-1
                break
            
            return
        
        if page<0:
            page=0
        elif page>=len(self.pages):
            page=len(self.pages)-1
        
        if self.page==page:
            return

        self.page=page
        self.task_flag=GUI_STATE_SWITCHING_PAGE
        
        try:
            await client.message_edit(message,embed=self.pages[page])
        except BaseException as err:
            self.task_flag=GUI_STATE_CANCELLED
            self.cancel()
            
            if isinstance(err,ConnectionError):
                # no internet
                return
            
            if isinstance(err,DiscordException):
                if err.code in (
                        ERROR_CODES.unknown_message, # message deleted
                        ERROR_CODES.unknown_channel, # channel deleted
                        ERROR_CODES.missing_access, # client removed
                            ):
                    return
            
            # We definitedly do not want to silence `ERROR_CODES.invalid_form_body`
            await client.events.error(client,f'{self!r}.__call__',err)
            return
        
        if self.task_flag==GUI_STATE_CANCELLING:
            self.task_flag=GUI_STATE_CANCELLED
            self.cancel()
            
            try:
                await client.message_delete(message)
            except BaseException as err:
                
                if isinstance(err,ConnectionError):
                    # no internet
                    return
                
                if isinstance(err,DiscordException):
                    if err.code in (
                            ERROR_CODES.unknown_channel, #message's channel deleted
                            ERROR_CODES.missing_access, # client removed
                                ):
                        return
                
                await client.events.error(client,f'{self!r}.__call__',err)
                return
            
            return
            
        self.task_flag=GUI_STATE_READY
        self.timeouter.set_timeout(self.timeout)
    
    async def _canceller(self,exception,):
        client=self.client
        message=self.message
        
        client.events.reaction_add.remove(message, self)
        client.events.reaction_delete.remove(message, self)
        
        if self.task_flag==GUI_STATE_SWITCHING_CTX:
            # the message is not our, we should not do anything with it.
            return
        
        self.task_flag=GUI_STATE_CANCELLED
        
        if exception is None:
            return
        
        if isinstance(exception,TimeoutError):
            if self.channel.cached_permissions_for(client).can_manage_messages:
                try:
                    await client.reaction_clear(message)
                except BaseException as err:
                    
                    if isinstance(err,ConnectionError):
                        # no internet
                        return
                    
                    if isinstance(err,DiscordException):
                        if err.code in (
                                ERROR_CODES.unknown_message, # message deleted
                                ERROR_CODES.unknown_channel, # channel deleted
                                ERROR_CODES.missing_access, # client removed
                                ERROR_CODES.missing_permissions, # permissions changed meanwhile
                                    ):
                            return
                    
                    await client.events.error(client,f'{self!r}._canceller',err)
                    return
            return
        
        timeouter=self.timeouter
        if timeouter is not None:
            timeouter.cancel()
        #we do nothing
    
    def cancel(self,exception=None):
        canceller=self.canceller
        if canceller is None:
            return
        
        self.canceller=None
        
        timeouter=self.timeouter
        if timeouter is not None:
            timeouter.cancel()
        
        return Task(canceller(self,exception),self.client.loop)
    
    def __repr__(self):
        result = [
            '<', self.__class__.__name__,
            ' pages=', repr(len(self.pages)),
            ', page=', repr(self.page),
            ', channel=', repr(self.channel),
            ', task_flag='
                ]
        
        task_flag=self.task_flag
        result.append(repr(task_flag))
        result.append(' (')
        
        task_flag_name = (
            'GUI_STATE_READY',
            'GUI_STATE_SWITCHING_PAGE',
            'GUI_STATE_CANCELLING',
            'GUI_STATE_CANCELLED',
            'GUI_STATE_SWITCHING_CTX',
                )[task_flag]
        
        result.append(task_flag_name)
        result.append(')>')
        
        return ''.join(result)
    
    async def _reaction_delete(self,emoji,user):
        client=self.client
        try:
            await client.reaction_delete(self.message,emoji,user)
        except BaseException as err:
            
            if isinstance(err,ConnectionError):
                # no internet
                return
            
            if isinstance(err,DiscordException):
                if err.code in (
                        ERROR_CODES.unknown_message, # message deleted
                        ERROR_CODES.unknown_channel, # channel deleted
                        ERROR_CODES.missing_access, # client removed
                        ERROR_CODES.missing_permissions, # permissions changed meanwhile
                            ):
                    return
            
            await client.events.error(client,f'{self!r}._reaction_delete',err)
            return

class WaitAndContinue(object):
    __slots__=('canceller', 'check', 'event', 'future', 'target', 'timeouter')
    def __init__(self, future, check, target, event, timeout):
        self.canceller=self.__class__._canceller
        self.future=future
        self.check=check
        self.event=event
        self.target=target
        self.timeouter=Timeouter(future._loop,self,timeout)
        event.append(target, self)
    
    async def __call__(self, client, *args):
        result = self.check(*args)
        if type(result) is bool:
            if not result:
                return
                
            if len(args)==1:
                self.future.set_result_if_pending(args[0],)
            else:
                self.future.set_result_if_pending(args,)
        
        else:
            args=(*args,result,)
            self.future.set_result_if_pending(args,)
        
        self.cancel()
        
    async def _canceller(self,exception):
        self.event.remove(self.target, self)
        if exception is None:
            self.future.set_result_if_pending(None)
            return
        
        self.future.set_exception_if_pending(exception)
        
        if not isinstance(exception,TimeoutError):
            return

        timeouter=self.timeouter
        if timeouter is not None:
            timeouter.cancel()
    
    def cancel(self):
        canceller=self.canceller
        if canceller is None:
            return
        
        timeouter=self.timeouter
        if timeouter is not None:
            timeouter.cancel()
        
        return Task(canceller(self,None),self.future._loop)

def wait_for_reaction(client,message,check,timeout):
    future=Future(client.loop)
    WaitAndContinue(future,check,message,client.events.reaction_add,timeout)
    return future

def wait_for_message(client,channel,check,timeout):
    future=Future(client.loop)
    WaitAndContinue(future,check,channel,client.events.message_create,timeout)
    return future

class prefix_by_guild(dict):
    __slots__=('default', 'orm',)
    
    def __init__(self,default,*orm):
        if type(default) is not str:
            raise TypeError (f'Default expected type str, got type {default.__class__.__name__}')
        self.default=default
        if orm:
            if len(orm)!=3:
                raise TypeError(f'Expected \'engine\', \'table\', \'model\' for orm, but got {len(orm)} elements')
            self.orm=orm
            Task(self._load_orm(),KOKORO)
            KOKORO.wakeup()
            
    def __call__(self,message):
        guild=message.guild
        if guild is not None:
            return self.get(guild.id,self.default)
        return self.default
    
    def __getstate__(self):
        return self.default
    def __setstate__(self,state):
        self.default=state
        self.orm=None
    
    def add(self,guild,prefix):
        guild_id=guild.id
        if guild_id in self:
            if prefix==self.default:
                del self[guild_id]
                if self.orm is not None:
                    Task(self._remove_prefix(guild_id),KOKORO)
                    KOKORO.wakeup()
                return True
            self[guild_id]=prefix
            if self.orm is not None:
                Task(self._modify_prefix(guild_id,prefix),KOKORO)
                KOKORO.wakeup()
            return True
        else:
            if prefix==self.default:
                return False
            self[guild_id]=prefix
            if self.orm is not None:
                Task(self._add_prefix(guild_id,prefix),KOKORO)
                KOKORO.wakeup()
            return True
    
    def to_json_serializable(self):
        result=dict(self)
        result['default']=self.default
        return result
    
    @classmethod
    def from_json_serialization(cls,data):
        self=dict.__new__(cls)
        self.default=data.pop('default')
        for id_,prefix in data.items():
            self[int(id_)]=prefix
        self.orm=None
        return self
    
    async def _load_orm(self,):
        engine,table,model=self.orm
        async with engine.connect() as connector:
            result = await connector.execute(table.select())
            prefixes = await result.fetchall()
            for item in prefixes:
                self[item.guild_id]=item.prefix
    
    async def _add_prefix(self,guild_id,prefix):
        engine,table,model=self.orm
        async with engine.connect() as connector:
            await connector.execute(table.insert(). \
                values(guild_id=guild_id,prefix=prefix))
    
    async def _modify_prefix(self,guild_id,prefix):
        engine,table,model=self.orm
        async with engine.connect() as connector:
            await connector.execute(table.update(). \
                values(prefix=prefix). \
                where(model.guild_id==guild_id))
    
    async def _remove_prefix(self,guild_id):
        engine,table,model=self.orm
        async with engine.connect() as connector:
            await connector.execute(table.delete(). \
                where(model.guild_id==guild_id))
    
    def __repr__(self):
        return f'<{self.__class__.__name__} default=\'{self.default}\' len={self.__len__()}>'
    
    # because it is a builtin subclass, it will have __str__, so we overwrite that as well
    __str__=__repr__
    
class _CD_unit(object):
    __slots__=('expires_at', 'uses_left',)
    def __init__(self,expires_at,uses_left):
        self.expires_at=expires_at
        self.uses_left=uses_left
    
    def __repr__(self):
        return f'{self.__class__.__name__}(expires_at={self.expires_at}, uses_left={self.uses_left})'

class Cooldown(MethodLike):
    __async_call__=True
    __wrapper__=1
    
    __slots__=('__func__', '__name__', 'cache', 'checker', 'handler', 'limit',
        'reset', 'weight',)
    
    async def _default_handler(client,message,command,time_left):
        return
    
    def __new__(cls,for_,reset,limit=1,weight=1,handler=_default_handler,name=None,func=None):
        if 'user'.startswith(for_):
            checker=cls._check_user
        elif 'channel'.startswith(for_):
            checker=cls._check_channel
        elif 'guild'.startswith(for_):
            checker=cls._check_guild
        else:
            raise ValueError(f'\'for_\' can be \'user\', \'channel\' or \'guild\', got {for_!r}')
        
        self=object.__new__(cls)
        self.checker=checker
        self.handler=handler
        
        if type(reset) is not float:
            reset=float(reset)
        
        self.reset=reset
        
        self.cache={}
        
        if type(weight) is not int:
            weight=int(weight)
        self.weight=weight
        
        if type(limit) is not int:
            limit=int(limit)
        self.limit=limit-weight
        
        if (name is not None) and (not name.islower()):
            name=name.lower()
        
        if func is None:
            self.__name__=name
            self.__func__=DEFAULT_EVENT
            return self._wrapper
        
        self.__name__=check_name(func,name)
        self.__func__ = func
        return self
    
    def _wrapper(self,func):
        name=self.__name__
        if (name is None) or (not name):
            self.__name__=check_name(func,None)
        self.__func__ = func
        return self
    
    def __call__(self,client,message,*args):
        loop=client.loop
        value=self.checker(self,message,loop)
        if value:
            return self.handler(client,message,self.__name__,value-loop.time())
        
        return self.__func__(client,message,*args)
    
    def shared(source,weight=0,name=None,func=None):
        self        = object.__new__(type(source))
        self.checker= source.checker
        self.reset  = source.reset
        self.cache  = source.cache
        if type(weight) is not int:
            weight=int(weight)
        if not weight:
            weight = source.weight
        self.weight = weight
        self.limit  = source.limit+source.weight-weight
        self.handler= source.handler
        
        if (name is not None) and (not name.islower()):
            name=name.lower()
        
        if func is None:
            self.__name__=name
            self.__func__=DEFAULT_EVENT
            return self._wrapper
        
        self.__name__=check_name(func,name)
        self.__func__ = func
    
    @property
    def __doc__(self):
        return getattr(self.__func__,'__doc__',None)
    
    @staticmethod
    def _check_user(self,message,loop):
        id_=message.author.id
        
        cache=self.cache
        try:
            unit=cache[id_]
        except KeyError:
            at_=loop.time()+self.reset
            cache[id_]=_CD_unit(at_,self.limit)
            loop.call_at(at_,cache.__delitem__,id_)
            return 0.
        
        left=unit.uses_left
        if left>0:
            unit.uses_left=left-self.weight
            return 0.
        return unit.expires_at
    
    @staticmethod
    def _check_channel(self,message,loop):
        id_=message.channel.id
        
        cache=self.cache
        try:
            unit=cache[id_]
        except KeyError:
            at_=loop.time()+self.reset
            cache[id_]=_CD_unit(at_,self.limit)
            loop.call_at(at_,cache.__delitem__,id_)
            return 0.
        
        left=unit.uses_left
        if left>0:
            unit.uses_left=left-self.weight
            return 0.
        return unit.expires_at
    
    #returns -1. if non guild
    @staticmethod
    def _check_guild(self,message,loop):
        channel=message.channel
        if channel.type in (1,3):
            return -1.
        else:
            id_=channel.guild.id
        
        cache=self.cache
        try:
            unit=cache[id_]
        except KeyError:
            at_=loop.time()+self.reset
            cache[id_]=_CD_unit(at_,self.limit)
            loop.call_at(at_,cache.__delitem__,id_)
            return 0.
        
        left=unit.uses_left
        if left>0:
            unit.uses_left=left-self.weight
            return 0.
        return unit.expires_at

def setup_extension(client, prefix, **kwargs):
    if type(client) is not Client:
        raise TypeError(f'Expected type `{Client.__name__}` as client, meanwhile got `{client!r}`.')
    
    if hasattr(client,'command_processer'):
        raise RuntimeError(f'The client already has an attribute named as `{"command_processer"!r}`.')
    
    if hasattr(client,'commands'):
        raise RuntimeError(f'The client already has an attribute named s `{"commands"!r}`.')
    
    event_message_create=client.events.message_create
    while True:
        if event_message_create is DEFAULT_EVENT:
            break
        
        if type(event_message_create) is asynclist:
            for event in event_message_create:
                if isinstance(event,CommandProcesser):
                    raise RuntimeError(f'The client already has a `{CommandProcesser.__name__}` instance added as event.')
            break
        
        if isinstance(event_message_create,CommandProcesser):
            raise RuntimeError(f'The client already has a `{CommandProcesser.__name__}` instance added as event.')
        
        break
    
    command_processer = client.events(CommandProcesser(prefix,**kwargs))
    client.command_processer=command_processer
    client.commands=command_processer.shortcut
    
    event_reaction_add = client.events.reaction_add
    while True:
        if event_reaction_add is DEFAULT_EVENT:
            client.events(ReactionAddWaitfor)
            break
        
        if type(event_reaction_add) is asynclist:
            for event in event_reaction_add:
                if isinstance(event,EventWaitforBase):
                    break
            else:
                client.events(ReactionAddWaitfor)
            
            break
        
        if isinstance(event_reaction_add,EventWaitforBase):
            break
        
        client.events(ReactionAddWaitfor)
        break
    
    event_reaction_delete = client.events.reaction_delete
    while True:
        if event_reaction_delete is DEFAULT_EVENT:
            client.events(ReactionDeleteWaitfor)
            break
        
        if type(event_reaction_delete) is asynclist:
            for event in event_reaction_add:
                if isinstance(event,EventWaitforBase):
                    break
            else:
                client.events(ReactionDeleteWaitfor)
            
            break
        
        if isinstance(event_reaction_delete,EventWaitforBase):
            break
        
        client.events(ReactionDeleteWaitfor)
        break
    
    return command_processer

del modulize, MethodLike
