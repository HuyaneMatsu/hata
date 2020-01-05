# -*- coding: utf-8 -*-
__all__ = ('CommandProcesser', 'ContentParser', 'Cooldown',
    'GUI_STATE_CANCELLED', 'GUI_STATE_CANCELLING', 'GUI_STATE_READY',
    'GUI_STATE_SWITCHING_CTX', 'GUI_STATE_SWITCHING_PAGE', 'Pagination',
    'ReactionAddWaitfor', 'ReactionDeleteWaitfor', 'WaitAndContinue',
    'multievent', 'prefix_by_guild', 'wait_for_message',
    'wait_for_reaction', )

import re
from weakref import WeakKeyDictionary

from .futures import Task, Future

from .others import USER_MENTION_RP
from .parsers import check_passed, EventHandlerBase, compare_converted,     \
    check_name, check_passed_tuple, asynclist, DEFAULT_EVENT
from .emoji import BUILTIN_EMOJIS
from .exceptions import DiscordException
from .client_core import KOKORO

#Invite this as well, to shortcut imports
from .events_compiler import ContentParser

COMMAND_RP=re.compile(' *([^ \t\\n]*) *(.*)')

#example
class CommandProcesser(EventHandlerBase):
    __slots__=('commands', 'default_event', 'ignorecase', 'invalid_command',
        'mention_prefix', 'prefix', 'prefixfilter', 'waitfors',)
    __event_name__='message_create'
    def __init__(self,prefix,ignorecase=True,mention_prefix=True):
        self.default_event=DEFAULT_EVENT
        self.invalid_command=DEFAULT_EVENT
        self.mention_prefix=mention_prefix
        self.waitfors=WeakKeyDictionary()
        self.commands={}
        self.update_prefix(prefix,ignorecase)
        self.ignorecase=ignorecase
        
    def update_prefix(self,prefix,ignorecase=None):
        if ignorecase is None:
            ignorecase=self.ignorecase
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
        self.ignorecase=ignorecase

    def __setevent__(self,func,case):
        #called every time, but only if every other fails
        if case=='default_event':
            func=check_passed(func,2,'\'default_event\' expects 2 arguments (client, message).')
            self.default_event=func
        #called when user used bad command after the preset prefix, called if a command fails
        elif case=='invalid_command':
            func=check_passed(func,4,'\'invalid_command\' expected 4 arguemnts (client, message, command, content).')
            self.invalid_command=func
        else:
            #called first
            argcount,func = check_passed_tuple(func,(3,2),)
            if argcount==2:
                needs_content=False
            else:
                needs_content=True
            self.commands[case]=(needs_content,func)
        
        return func
    
    def __delevent__(self,func,case):
        if case=='default_event':
            if func is self.default_event:
                self.default_event=DEFAULT_EVENT
            else:
                raise ValueError(f'The passed \'{case}\' ({func!r}) is not the same as the already loaded one: {self.default_event!r}')
        
        elif case=='invalid_command':
            if func is self.invalid_command:
                self.invalid_command=DEFAULT_EVENT
            else:
                raise ValueError(f'The passed \'{case}\' ({func!r}) is not the same as the already loaded one: {self.invalid_command!r}')
        
        else:
            try:
                argcount,actual=self.commands[case]
            except KeyError as err:
                raise ValueError(f'The passed \'{case}\' is not added as a command right now.')
            
            if compare_converted(actual,func):
                del self.commands[case]
            else:
                raise ValueError(f'The passed \'{case}\' ({func!r}) command is not the same as the already loaded one: {actual!r}')
            
    async def __call__(self,client,message):
        try:
            event=self.waitfors[message.channel]
        except KeyError:
            pass
        else:
            if type(event) is asynclist:
                for event in event:
                    Task(event(client,message,),client.loop)
            else:
                Task(event(client,message,),client.loop)
        
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
                
                command,content=result.groups()
                command=command.lower()
                
                try:
                    needs_content,event=self.commands[command]
                except KeyError:
                    break
                
                if needs_content:
                    await event(client,message,content)
                else:
                    await event(client,message)
                return
        
        else:
            command,content=result
            command=command.lower()
            
            try:
                needs_content,event=self.commands[command]
            except KeyError:
                return (await self.invalid_command(client,message,command,content))

            if needs_content:
                await event(client,message,content)
            else:
                await event(client,message)
            return
        
        return (await self.default_event(client,message))
    
    async def call_command(self,command_name,client,message,content=''):
        if not command_name.islower():
            command_name=command_name.lower()
        
        try:
            needs_content,event=self.commands[command_name]
        except KeyError:
            raise LookupError(command_name) from None

        if needs_content:
            await event(client,message,content)
        else:
            await event(client,message)
    
    def append(self,wrapper,target):
        try:
            actual=self.waitfors[target]
            if type(actual) is asynclist:
                actual.append(wrapper)
            else:
                self.waitfors[target]=container=asynclist()
                container.append(actual)
                container.append(wrapper)
        except KeyError:
            self.waitfors[target]=wrapper

    def remove(self,wrapper,target,):
        try:
            container=self.waitfors.pop(target)
            if type(container) is asynclist:
                container.remove(wrapper)
                if len(container)==1:
                    self.waitfors[target]=container[0]
                else:
                    self.waitfors[target]=container
        except (KeyError,ValueError):
            #`KeyError` if `target` is missing
            #`ValueError` if `wrapper` is missing
            pass
    
    def __repr__(self):
        result = [
            '<', self.__class__.__name__,
            ' prefix=', repr(self.prefix),
            ', command count=', repr(len(self.commands)),
            ', mention_prefix=', repr(self.mention_prefix),
                ]
        
        default_event=self.default_event
        if default_event is not DEFAULT_EVENT:
            result.append(', default_event=')
            result.append(default_event.__repr__())
        
        invalid_command=self.invalid_command
        if invalid_command is not DEFAULT_EVENT:
            result.append(', invalid_command=')
            result.append(invalid_command.__repr__())
        
        result.append('>')
        
        return ''.join(result)
        
class ReactionAddWaitfor(EventHandlerBase):
    __slots__=('waitfors',)
    __event_name__='reaction_add'
    
    def __init__(self):
        self.waitfors=WeakKeyDictionary()
    
    append=CommandProcesser.append
    remove=CommandProcesser.remove
    
    async def __call__(self,client,message,emoji,user):
        try:
            event=self.waitfors[message]
        except KeyError:
            return

        if type(event) is asynclist:
            for event in event:
                Task(event(client,emoji,user,),client.loop)
        else:
            Task(event(client,emoji,user,),client.loop)
            
class ReactionDeleteWaitfor(EventHandlerBase):
    __slots__=('waitfors',)
    __event_name__='reaction_delete'
    
    def __init__(self):
        self.waitfors=WeakKeyDictionary()
    
    append  = ReactionAddWaitfor.append
    remove  = ReactionAddWaitfor.remove
    __call__= ReactionAddWaitfor.__call__

class multievent(object):
    __slots__=('events',)
    
    def __init__(self,*events):
        self.events=events
        
    def append(self,wrapper,target):
        for event in self.events:
            event.append(wrapper,target)
    
    def remove(self,wrapper,target):
        for event in self.events:
            event.remove(wrapper,target)

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
        'task_flag', 'timeouter')
    
    async def __new__(cls,client,channel,pages,timeout=240.,message=None):
        self=object.__new__(cls)
        self.client=client
        self.channel=channel
        self.pages=pages
        self.page=0
        self.canceller=cls._canceller
        self.task_flag=GUI_STATE_READY
        self.message=message
        self.timeouter=None
        
        if message is None:
            message = await client.message_create(channel,embed=pages[0])
            self.message=message
        
        if not channel.cached_permissions_for(client).can_add_reactions:
            return self

        message.weakrefer()
        
        if len(self.pages)>1:
            for emoji in self.EMOJIS:
                await client.reaction_add(message,emoji)
        else:
            await client.reaction_add(message,self.CANCEL)
        
        self.timeouter=Timeouter(client.loop,self,timeout=timeout)
        client.events.reaction_add.append(self,message)
        client.events.reaction_delete.append(self,message)
        return self
    
    async def __call__(self,client,emoji,user):
        if user.is_bot or (emoji not in self.EMOJIS):
            return
        
        message=self.message
        
        can_manage_messages=self.channel.cached_permissions_for(client).can_manage_messages
        if can_manage_messages:
            if not message.did_react(emoji,user):
                return
            Task(self.reaction_remove(client,message,emoji,user),client.loop)
        
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
                except DiscordException:
                    pass
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
        except DiscordException:
            self.task_flag=GUI_STATE_CANCELLED
            self.cancel()
            return
        
        if self.task_flag==GUI_STATE_CANCELLING:
            self.task_flag=GUI_STATE_CANCELLED
            if can_manage_messages:
                try:
                    await client.message_delete(message)
                except DiscordException:
                    pass

            self.cancel()
            return
            
        self.task_flag=GUI_STATE_READY
        
        timeouter=self.timeouter
        if timeouter.timeout<240.:
            timeouter.timeout+=30.
            
    @staticmethod
    async def reaction_remove(client,message,emoji,user):
        try:
            await client.reaction_delete(message,emoji,user)
        except DiscordException:
            pass
    
    async def _canceller(self,exception,):
        client=self.client
        message=self.message
        
        client.events.reaction_add.remove(self,message)
        client.events.reaction_delete.remove(self,message)
        
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
                except DiscordException:
                    pass
            return
        
        timeouter=self.timeouter
        if timeouter is not None:
            timeouter.cancel()
        #we do nothing
    
    def cancel(self):
        canceller=self.canceller
        if canceller is None:
            return
        
        self.canceller=None
        
        timeouter=self.timeouter
        if timeouter is not None:
            timeouter.cancel()
        
        return Task(canceller(self,None),self.client.loop)
    
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

class WaitAndContinue(object):
    __slots__=('canceller', 'check', 'event', 'future', 'target', 'timeouter')
    def __init__(self, future, check, target, event, timeout):
        self.canceller=self.__class__._canceller
        self.future=future
        self.check=check
        self.event=event
        self.target=target
        self.timeouter=Timeouter(future._loop,self,timeout)
        event.append(self,target)
        
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
        self.event.remove(self,self.target)
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


def wait_for_reaction(client,message,case,timeout):
    future=Future(client.loop)
    WaitAndContinue(future,case,message,client.events.reaction_add,timeout)
    return future

def wait_for_message(client,channel,case,timeout):
    future=Future(client.loop)
    WaitAndContinue(future,case,channel,client.events.message_create,timeout)
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
    
class Cooldown(object):
    __async_call__=True
    
    __slots__=('__func__', '__name__', 'cache', 'checker', 'handler', 'limit',
        'reset', 'weight',)
    
    async def _default_handler(client,message,command,time_left):
        return
    
    def __new__(cls,for_,reset,limit=1,weight=1,handler=_default_handler,case=None,func=None):
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
        
        if (case is not None) and (not case.islower()):
            case=case.lower()
        
        if func is None:
            self.__name__=case
            self.__func__=DEFAULT_EVENT
            return self._wrapper
        
        self.__name__=check_name(func,case)
        self.__func__=check_passed(func,3)
        return self

    def _wrapper(self,func):
        if not self.__name__:
            self.__name__=check_name(func,None)
        self.__func__=check_passed(func,3)
        return self
    
    def __call__(self,client,message,*args):
        loop=client.loop
        value=self.checker(self,message,loop)
        if value:
            return self.handler(client,message,self.__name__,value-loop.time())
        else:
            return self.__func__(client,message,*args)
    
    def shared(source,weight=0,case=None,func=None):
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
        
        if (case is not None) and (not case.islower()):
            case=case.lower()
            
        if func is None:
            self.__name__=case
            self.__func__=DEFAULT_EVENT
            return self._wrapper
        
        self.__name__=check_name(func,case)
        self.__func__=check_passed(func,3)
    
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
