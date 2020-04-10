# -*- coding: utf-8 -*-
__all__ = ('Category', 'Command', 'CommandProcesser', 'checks', 'normalize_description', )

import re, reprlib

from ...backend.dereaddons_local import sortedlist, modulize
from ...backend.futures import Task

from ...discord.others import USER_MENTION_RP
from ...discord.parsers import EventWaitforBase, compare_converted, check_name, check_argcount_and_convert, DEFAULT_EVENT
from ...discord.guild import Guild
from ...discord.permission import Permission
from ...discord.role import Role
from ...discord.channel import ChannelBase

from .compiler import parse, COMMAND_CALL_SETTING_2ARGS, COMMAND_CALL_SETTING_3ARGS, COMMAND_CALL_SETTING_USE_PARSER

COMMAND_RP=re.compile(' *([^ \t\\n]*) *(.*)')

class Command(object):
    __slots__ = ( '_call_setting', '_category_hint', '_check_failure_handler',
        '_checks', '_parser', '_parser_failure_handler', 'aliases', 'category',
        'command', 'description', 'name', )
    
    @classmethod
    def from_class(cls, klass, kwargs=None):
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
        
        if (kwargs is not None) and kwargs:
            if (description is None):
                description = kwargs.pop('description', None)
            else:
                try:
                    del kwargs['description']
                except KeyError:
                    pass
            
            if (category is None):
                category = kwargs.pop('category', None)
            else:
                try:
                    del kwargs['category']
                except KeyError:
                    pass
            
            if (checks_ is None) or not checks_:
                checks_ = kwargs.pop('checks', None)
            else:
                try:
                    del kwargs['checks']
                except KeyError:
                    pass
            
            if (check_failure_handler is None):
                check_failure_handler = kwargs.pop('check_failure_handler', None)
            else:
                try:
                    del kwargs['check_failure_handler']
                except KeyError:
                    pass
            
            if (parser_failure_handler is None):
                parser_failure_handler = kwargs.pop('parser_failure_handler', None)
            else:
                try:
                    del kwargs['parser_failure_handler']
                except KeyError:
                    pass
            
            if kwargs:
                raise TypeError(f'`{cls.__name__}.from_class` did not use up some kwargs: `{list(kwargs)!r}`.')
        
        return cls(command, name, description, aliases, category, checks_, check_failure_handler, parser_failure_handler)
    
    @classmethod
    def from_kwargs(cls, command, name, kwargs):
        if (kwargs is None) or (not kwargs):
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
                raise TypeError(f'type `{cls.__name__}` not uses: `{list(kwargs)!r}`.')
        
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
            '`parser_failure_handler` expected 5 arguemnts (client, message, command, content, args).')
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
    __slots__ = ('_default_category_name', '_ignorecase', 'categories', 'command_error', 'commands', 'default_event',
        'get_prefix_for', 'invalid_command', 'mention_prefix', 'prefix', 'prefixfilter', )
    
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
                
                get_prefix_for = prefix
                break
            
            if type(prefix) is str:
                if not prefix:
                    raise ValueError('Prefix cannot be passed as empty string.')
                
                PREFIX_RP=re.compile(re.escape(prefix),flag)
                def get_prefix_for(message):
                    return practical_prefix
            
            elif isinstance(prefix,(list,tuple)):
                if not prefix:
                    raise ValueError(f'Prefix fed as empty {prefix.__class__.__name__}: {prefix!r}')
                
                for prefix_ in prefix:
                    if type(prefix_) is not str:
                        raise TypeError(f'Prefix can be only callable, str or tuple/list type of str, got {prefix_!r}')
                    
                    if not prefix_:
                        raise ValueError('Prefix cannot be passed as empty string.')
                
                PREFIX_RP=re.compile("|".join(re.escape(prefix_) for prefix_ in prefix),flag)
                practical_prefix = prefix[0]
                
                def get_prefix_for(message):
                    result=PREFIX_RP.match(message.content)
                    if result is None:
                        return practical_prefix
                    else:
                        return result.group(0)
            else:
                raise TypeError(f'Prefix can be only callable, str or tuple/list type of str, got {prefix!r}')
            
            def prefixfilter(message):
                content = message.content
                result=PREFIX_RP.match(content)
                if result is None:
                    return
                result=COMMAND_RP.match(content,result.end())
                if result is None:
                    return
                return result.groups()
            
            break
        
        self.prefix=prefix
        self.prefixfilter=prefixfilter
        self.get_prefix_for=get_prefix_for
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

del modulize
