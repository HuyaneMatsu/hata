# -*- coding: utf-8 -*-
__all__ = ('Converter', 'ConverterFlag', 'ContentParser', )

#TODO: ask python for GOTO already
import re
from datetime import timedelta

try:
    from dateutil.relativedelta import relativedelta
except ImportError:
    relativedelta = None
    
from ...backend.dereaddons_local import code, function, method, _spaceholder, NoneType, MethodLike
from ...backend.analyzer import CallableAnalyzer

from ...discord.bases import FlagBase
from ...discord.others import USER_MENTION_RP, ROLE_MENTION_RP, CHANNEL_MENTION_RP, IS_ID_RP
from ...discord.client import Client
from ...discord.exceptions import DiscordException
from ...discord.emoji import parse_emoji, Emoji, EMOJIS
from ...discord.client_core import CACHE_USER, USERS
from ...discord.message import Message
from ...discord.channel import ChannelBase, CHANNEL_TYPES
from ...discord.user import User
from ...discord.guild import Guild
from ...discord.role import Role
from ...discord.webhook import Webhook
from ...discord.oauth2 import UserOA2
from ...discord.parsers import check_argcount_and_convert

REQUEST_OVER = 50000
INT_CONVERSION_LIMIT = 100

DELTA_RP=re.compile('([\+\-]?\d+) *([a-zA-Z]+)')
PARSER_RP=re.compile('(?:"(.+?)"|(\S+))[^"\S]*')

TDELTA_KEYS=('weeks','days','hours','minutes','seconds','microseconds')
def parse_tdelta(part):
    result={}
    index=0
    limit=len(TDELTA_KEYS)
    for amount,name in DELTA_RP.findall(part):
        name=name.lower()
        if index==limit:
            break
        while True:
            key=TDELTA_KEYS[index]
            index+=1
            if key.startswith(name):
                result.setdefault(key,int(amount))
                break
            if index==limit:
                break

    if result:
        return timedelta(**result)

if (relativedelta is not None):
    RDELTA_KEYS=('years','months',)+TDELTA_KEYS
    
    def parse_rdelta(part):
        result={}
        index=0
        limit=len(RDELTA_KEYS)
        for amount,name in DELTA_RP.findall(part):
            name=name.lower()
            if index==limit:
                break
            while True:
                key=RDELTA_KEYS[index]
                index+=1
                if key.startswith(name):
                    result.setdefault(key,int(amount))
                    break
                if index==limit:
                    break
    
        if result:
            return relativedelta(**result)

    
class _eval_tester_cls(object):
    __slots__=('name', 'types',)
    def __init__(self,types,name=None):
        if types is None:
            pass
        elif type(types) is not tuple:
            types=(types,)
        object.__setattr__(self,'types',types)
        object.__setattr__(self,'name',name)
    def __getattribute__(self,name):
        types=object.__getattribute__(self,'types')
        if types is None:
            return type(self)(None)
        for type_ in types:
            if hasattr(type_,'__slots__'):
                if name in type_.__slots__:
                    return type(self)(None)
                if '__dict__' in type_.__slots__:
                    return type(self)(None)
            try:
                result=getattr(type_,name)
            except AttributeError as err:
                pass
            else:
                if type(result) is function:
                    return method(self,result)
                return result
        raise AttributeError(object.__getattribute__(self,'name'),name)
    def __setattr__(self,name,value):
        type(self).__getattribute__(self,name)
    def __delattr__(self,name):
        type(self).__getattribute__(self,name)
    def __call__(self,*args,**kwargs):
        if object.__getattribute__(self,'types') is not None:
            type(self).__getattribute__(self,'__call__')
        return type(self)(None)
    def __format__(self,code):
        return ''

def parse_user_mention(part,message):
    user_mentions=message.user_mentions
    if user_mentions is None:
        return
    
    parsed=USER_MENTION_RP.fullmatch(part)
    if parsed is None:
        return

    user_id=int(parsed.group(1))
    for user in user_mentions:
        if user.id==user_id:
            return user

def parse_role_mention(part,message):
    role_mentions=message.role_mentions
    if role_mentions is None:
        return
    
    parsed=ROLE_MENTION_RP.fullmatch(part)
    if parsed is None:
        return

    role_id=int(parsed.group(1))
    for role in role_mentions:
        if role.id==role_id:
            return role

def parse_channel_mention(part,message):
    channel_mentions=message.channel_mentions
    if channel_mentions is None:
        return
    
    parsed=CHANNEL_MENTION_RP.fullmatch(part)
    if parsed is None:
        return

    channel_id=int(parsed.group(1))
    for channel in channel_mentions:
        if channel.id==channel_id:
            return channel
        
PARSER_GLOBAL_DEFUALTS_OBJECTS = {}

_globals = {
    'USERS'                 : USERS,
    'parse_user_mention'    : parse_user_mention,
    'parse_role_mention'    : parse_role_mention,
    'parse_channel_mention' : parse_channel_mention,
    'DiscordException'      : DiscordException,
    'parse_emoji'           : parse_emoji,
    'parse_tdelta'          : parse_tdelta,
    'PARSER_RP'             : PARSER_RP,
    'IS_ID_RP'              : IS_ID_RP,
    'REQUEST_OVER'          : REQUEST_OVER,
    'INT_CONVERSION_LIMIT'  : INT_CONVERSION_LIMIT,
    'OBJECTS'               : PARSER_GLOBAL_DEFUALTS_OBJECTS,
    'EMOJIS'                : EMOJIS,
        }

if (relativedelta is not None):
    _globals['parse_rdelta']=parse_rdelta

_indexed_optional = {
    'user'      : _eval_tester_cls((User,Client,Webhook,UserOA2,),'user'),
    'role'      : _eval_tester_cls(Role,'role'),
    'channel'   : _eval_tester_cls(tuple(CHANNEL_TYPES),'channel'),
    'emoji'     : _eval_tester_cls(Emoji,'emoji'),
    'str'       : _eval_tester_cls(str,'str'),
    'int'       : _eval_tester_cls(int,'int'),
    'tdelta'    : _eval_tester_cls(timedelta,'tdelta'),
        }

if (relativedelta is not None):
    _indexed_optional['rdelta']=_eval_tester_cls(relativedelta,'rdelta')

_unindexed_static = {
    'client'    : _eval_tester_cls(Client,'client'),
    'message'   : _eval_tester_cls(Message,'message'),
    'content'   : _eval_tester_cls(str,'content'),
    'index'     : _eval_tester_cls(int,'index'),
    'limit'     : _eval_tester_cls(int,'limit'),
        }

_unindexed_optional = {
    'part'      : _eval_tester_cls(str,'part'),
    'guild'     : _eval_tester_cls(Guild,'guild'),
    'rest'      : _eval_tester_cls(str,'rest'),
        }

del USERS, DiscordException, parse_emoji, IS_ID_RP, Webhook, UserOA2, CHANNEL_TYPES

PARSER_FLAG_KEYS = {
    'guild'     : 0,
    'mention'   : 1,
    'name'      : 2,
    'id'        : 3,
    'everywhere': 4,
    'profile'   : 5,
    'reversed'  : 6,
        }

class ConverterFlag(FlagBase):
    __keys__ = {
        'guild'     : 0,
        'mention'   : 1,
        'name'      : 2,
        'id'        : 3,
        'everywhere': 4,
        'profile'   : 5,
        'reversed'  : 6,
            }
    
    user_default = NotImplemented
    role_default = NotImplemented
    channel_default = NotImplemented
    guild_default = NotImplemented
    emoji_default = NotImplemented

ConverterFlag.user_default = ConverterFlag().update_by_keys(mention=True, name=True, id=True)
ConverterFlag.role_default = ConverterFlag().update_by_keys(guild=True, mention=True, name=True, id=True)
ConverterFlag.channel_default = ConverterFlag().update_by_keys(guild=True, mention=True, name=True, id=True)
ConverterFlag.guild_default = ConverterFlag().update_by_keys(guild=True)
ConverterFlag.emoji_default = ConverterFlag().update_by_keys(mention=True, name=True, id=True)

class ParserMeta(object):
    INSTANCES = {}
    
    __slots__=('name', 'flags_must', 'flags_default', 'flags_all',
        'passing_enabled', 'amount_enabled', 'default_enabled',)
    
    def __init__(self, name, flags_must, flags_default, flags_all, amount_enabled,):
        self.INSTANCES[name]= self
        self.name           = name
        self.flags_must     = flags_must
        self.flags_default  = flags_default
        self.flags_all      = flags_all
        self.amount_enabled = amount_enabled
    
    def validate_flags(self, value):
        flags_must = self.flags_must
        flags_all = self.flags_all
        
        for push in PARSER_FLAG_KEYS.values():
            if (value>>push)&1:
                if not (flags_all>>push)&1:
                    value = value^(1<<push)
            else:
                if (flags_must>>push)&1:
                    value = value|(1<<push)
        
        if value==0:
            return self.flags_must
        
        return ConverterFlag(value)
    
    def validate_amount(self, value):
        if not self.amount_enabled:
            return 1
        
        return value
    
    def validate_default(self, default_value, default_type):
        if default_type is ConverterDefaultType.object:
            if type(default_value) in (NoneType,int,str):
                default_value=repr(default_value)
                default_type=ConverterDefaultType.code
            else:
                default_value=DefaultValue(default_value)
        
        return default_value, default_type
    
ParserMeta('user', ConverterFlag(), ConverterFlag.user_default, ConverterFlag.user_default.update_by_keys(guild=True, everywhere=True, profile=True), True, )
ParserMeta('role', ConverterFlag.guild_default, ConverterFlag.role_default, ConverterFlag.role_default, True,  )
ParserMeta('channel', ConverterFlag.guild_default, ConverterFlag.channel_default, ConverterFlag.channel_default, True, )
ParserMeta('guild', ConverterFlag.guild_default, ConverterFlag.guild_default, ConverterFlag.guild_default, False, )
ParserMeta('emoji', ConverterFlag(), ConverterFlag.emoji_default, ConverterFlag.emoji_default.update_by_keys(guild=True, everywhere=True), True, )
ParserMeta('content', ConverterFlag(), ConverterFlag(), ConverterFlag(), False, )
ParserMeta('rest', ConverterFlag(), ConverterFlag(), ConverterFlag(), False, )
ParserMeta('str', ConverterFlag(), ConverterFlag(), ConverterFlag(), True, )
ParserMeta('int', ConverterFlag(), ConverterFlag(), ConverterFlag(), True, )
ParserMeta('tdelta', ConverterFlag(), ConverterFlag(), ConverterFlag(), True, )

if (relativedelta is not None):
    ParserMeta('rdelta', ConverterFlag(), ConverterFlag(), ConverterFlag(), True, )

COMMAND_CALL_SETTING_2ARGS      = 0
COMMAND_CALL_SETTING_3ARGS      = 1
COMMAND_CALL_SETTING_USE_PARSER = 2

ANNOTATION_TO_TYPE_TO_NAME = {
    Client      : 'client',
    User        : 'user',
    Role        : 'role',
    ChannelBase : 'channel',
    Guild       : 'guild',
    Message     : 'message',
    Emoji       : 'emoji',
    str         : 'str',
    int         : 'int',
    timedelta   : 'tdelta',
        }

if (relativedelta is not None):
    ANNOTATION_TO_TYPE_TO_NAME[relativedelta] = 'rdelta'

class ConverterDefaultType(object):
    __slots__ = ()
    
    none = NotImplemented
    object = NotImplemented
    code = NotImplemented

ConverterDefaultType.none = ConverterDefaultType()
ConverterDefaultType.object = ConverterDefaultType()
ConverterDefaultType.code = ConverterDefaultType()

class DefaultValue(object):
    _object_id_counter = 0
    __slots__ = ('id', 'value', )
    
    def __new__(cls,value):
        id_ = cls._object_id_counter
        cls._object_id_counter=id_+1
        
        self=object.__new__(cls)
        self.value=value
        self.id=id_
        
        PARSER_GLOBAL_DEFUALTS_OBJECTS[id_]=value
        
        return self
    
    def __del__(self):
        try:
            del PARSER_GLOBAL_DEFUALTS_OBJECTS[self.id]
        except KeyError:
            pass
    
    def __str__(self):
        return f'OBJECTS[{self.id}]'
    
    def __repr__(self):
        return f'{self.__class__.__name__}({self.value})'

class Converter(object):
    __slots__ = ('args', 'amount', 'default_type', 'default_value', 'flags', 'meta',)
    def __new__(cls, type_, flags=None, default=_spaceholder, amount = None, default_code=None):
        if not isinstance(type_,str):
            raise TypeError('`type_` should have been passed as `str` instance.')
        
        if not type_.islower():
            type_ = type_.lower()
        
        try:
            meta = ParserMeta.INSTANCES[type_]
        except KeyError:
            raise ValueError(f'Not supported type: `{type_!r}`.') from None
        
        if flags is None:
            flags = meta.flags_default
        else:
            if not isinstance(flags,int):
                raise TypeError(f'`flags` should have been passed as `int` instance or `None`, got `{flags!r}`.')
            
            if type(flags) is not ConverterFlag:
                flags = ConverterFlag(flags)
            
            flags = meta.validate_flags(flags)
        
        if default is _spaceholder:
            if default_code is None:
                default_type = ConverterDefaultType.none
            else:
                default_type = ConverterDefaultType.code
        else:
            if default_code is None:
                default_type = ConverterDefaultType.object
            else:
                raise ValueError(f'`default` and `default_code` are mutually exclusive.')
        
        if default_type is ConverterDefaultType.none:
            default_value = None
        elif default_type is ConverterDefaultType.code:
            if not isinstance(default_code,str):
                raise TypeError(f'`default_code` should have been passed as `str` instance or `None`, got `{default_code!r}`˙.')
        
            default_value = default_code
        else:
            default_value=default
        
        default_value, default_type = meta.validate_default(default_value, default_type)
        
        if (amount is None):
            amount = 1
        
        elif isinstance(amount,int):
            if type(amount) is not int:
                amount = int(amount)
            
            if amount<1:
                raise ValueError(f'`amount` cannot be negative or `0`, got {amount!r}`.')
            
        elif isinstance(amount,tuple):
            if type(amount) is not tuple:
                amount=tuple(amount)
                
            if len(amount)!=2:
                raise TypeError(f'`amount` should have been passed as `tuple` instance of length 2, `int` instance or as `None`, got `{amount!r}`.')
            
            min_, max_ = amount
            if min_ < 0 or max_ < 0:
                raise ValueError(f'`amount` cannot be negative or `0`, got {amount!r}')
            
            if min_ != 0 and max_ !=0:
                if min_ == max_:
                    amount = min_
                
                if max_ > min_:
                    raise ValueError(f'`amount`\'s `min` value lower than `max` : {amount!r}`.')
                
        else:
            raise TypeError(f'`amount` should have been passed as `tuple` instance of length 2, `int` instance or as `None`, got `{amount!r}`.')
        
        amount = meta.validate_amount(amount)
        
        self = object.__new__(cls)
        self.args = False
        self.amount = amount
        self.default_type = default_type
        self.default_value = default_value
        self.flags = flags
        self.meta = meta
        return self
    
    def set_default(self, default_value):
        if self.default_type is not ConverterDefaultType.none:
            raise ValueError(f'The converter has already a default added.')
        
        default_value, default_type = self.meta.validate_default(default_value, ConverterDefaultType.object)
        
        self.default_value=default_value
        self.default_type=default_type
    
    def set_args(self):
        amount=self.amount
        if type(amount) is int and amount==1:
            self.amount = self.meta.validate_amount(0)
        
        self.args=True
    
    args_str = NotImplemented
    content = NotImplemented
    rest = NotImplemented
    str = NotImplemented
    
    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        if self.args != other.args:
            return False
        
        if self.flags!=other.flags:
            return False
        
        self_amount=self.amount
        other_amount=other.amount
        if type(self_amount) is int:
            if type(other_amount) is int:
                if self_amount!=other_amount:
                    return False
            else:
                return False
        else:
            if type(other_amount) is int:
                return False
            else:
                if self_amount!=other_amount:
                    return False
        
        self_default_type = self.default_type
        if self_default_type is not other.default_type:
            return False
        
        if self_default_type is not ConverterDefaultType.none:
            if self.default_value!=other.default_value:
                return False
        
        if self.meta is not other.meta:
            return False
        
        return True
    
    def __hash__(self):
        result = self.flags+(self.args<<11)
        
        amount = self.amount
        if type(amount) is int:
            result = result+(amount<<22)
        else:
            result = result^hash(result)
        
        if self.default_type is not ConverterDefaultType.none:
            result = result^hash(self.default_value)
        
        result = result^hash(self.meta.name)
        
        return result
    
    def __repr__(self):
        result = ['<',self.__class__.__name__,' ',self.meta.name,]
        
        if self.args:
            result.append(' (args arument)')
        else:
            amount = self.amount
            if (type(amount) is not int) or (amount!=1):
                result.append(' amount=')
                result.append(repr(amount))
                result.append(',')
        
        default_type=self.default_type
        if (default_type is not ConverterDefaultType.none):
            if default_type is ConverterDefaultType.code:
                result.append(' default (code)=')
            else:
                result.append(' default (object)=')
            
            result.append(repr(self.default_value))
            result.append(',')
        
        result.append(' flags=')
        result.append(repr(self.flags))
        
        result.append('>')
        return ''.join(result)
    
    def check_default(self,_locals):
        try:
            eval(self.default_value,_globals,_locals)
        except AttributeError as err:
            args=err.args
            if len(args)==2:
                err.args=(f'type {args[0]} has no attribute {args[1]!r}.',)
            raise
        except NameError:
            raise
        except Exception:
            pass
    
    @property
    def parse_one(self):
        amount = self.amount
        if type(amount) is not int:
            return False
        
        if amount!=1:
            return False
        
        return True
    
    @property
    def lower_limit(self):
        amount = self.amount
        if type(amount) is int:
            return amount
        
        return amount[0]

    @property
    def upper_limit(self):
        amount = self.amount
        if type(amount) is int:
            return amount
        
        return amount[1]
    
    @property
    def name(self):
        return self.meta.name
    
converter = object.__new__(Converter)
converter.args = True
converter.amount = 0
converter.default_type = ConverterDefaultType.none
converter.default_value = None
converter.flags = ConverterFlag()
converter.meta = ParserMeta.INSTANCES['str']
Converter.args_str = converter

converter = object.__new__(Converter)
converter.args = False
converter.amount = 0
converter.default_type = ConverterDefaultType.none
converter.default_value = None
converter.flags = ConverterFlag()
converter.meta = ParserMeta.INSTANCES['content']
Converter.content = converter

converter = object.__new__(Converter)
converter.args = False
converter.amount = 0
converter.default_type = ConverterDefaultType.none
converter.default_value = None
converter.flags = ConverterFlag()
converter.meta = ParserMeta.INSTANCES['rest']
Converter.rest = converter

converter = object.__new__(Converter)
converter.args = False
converter.amount = 0
converter.default_type = ConverterDefaultType.none
converter.default_value = None
converter.flags = ConverterFlag()
converter.meta = ParserMeta.INSTANCES['str']
Converter.str = converter

del converter

COMPILED_PARSERS = {}
    
def parse(func):
    analyzer = CallableAnalyzer(func)
    if analyzer.is_async():
        real_analyzer=analyzer
        should_instance=False
    elif analyzer.can_instance_to_async_callable():
        real_analyzer=CallableAnalyzer(func.__call__, as_method=True)
        if not real_analyzer.is_async():
            raise ValueError(f'Not async callable type, or cannot be instanced to async: `{func!r}`.')
        should_instance=True
    else:
        raise ValueError(f'Not async callable type, or cannot be instanced to async: `{func!r}`.')
    
    keyword_only_argument_count = real_analyzer.get_non_default_keyword_only_argument_count()
    if keyword_only_argument_count:
        raise ValueError(f'The passed callable: `{real_analyzer.real_func!r}` accepts keyword only arguments.')
    
    arguments = real_analyzer.get_non_reserved_positional_arguments()
    args_argument = real_analyzer.args_argument
    
    argument_count = len(arguments)
    if argument_count<2:
        raise ValueError(f'The passed callable: `{real_analyzer.real_func!r}` should accept at least 2 arguments, `client` an `message` (args ignored).')
    
    client_argument = arguments[0]
    if client_argument.has_default:
        raise ValueError(f'The passed callable: `{real_analyzer.real_func!r}` has default argument set as it\'s first not reserved, meanwhile it should not have.')
    
    if client_argument.has_annotation and client_argument.annoation is not Client:
        raise ValueError(f'The passed callable: `{real_analyzer.real_func!r}` has annotation at the client\'s argument slot, what is not `{Client.__name__}`.')
    
    message_argument = arguments[1]
    if message_argument.has_default:
        raise ValueError(f'The passed callable: `{real_analyzer.real_func!r}` has default argument set as it\'s first not reserved, meanwhile it should not have.')
    
    if message_argument.has_annotation and message_argument.annoation is not Message:
        raise ValueError(f'The passed callable: `{real_analyzer.real_func!r}` has annotation at the message\'s argument slot what is not `{Message.__name__}`.')
    
    parsed_arguments = []
    
    to_check=arguments[2:]
    to_check.append(args_argument)
    
    index = 0
    limit = len(to_check)
    while True:
        if index==limit:
            break
        argument = to_check[index]
        index = index+1
        
        if argument is None:
            break
        
        if argument.has_annotation:
            annotation = argument.annotation
            if issubclass(type(annotation),type):
                try:
                    type_ = ANNOTATION_TO_TYPE_TO_NAME[annotation]
                except KeyError:
                    raise ValueError(f'The passed callable `{real_analyzer.real_func!r}` has annotation to type `{annotation!r}`, which is not supported.')
                
                try:
                    meta = ParserMeta.INSTANCES[type_]
                except KeyError:
                    raise ValueError(f'Not passed callable would user a not supported type: `{type_!r}`.') from None

                if argument.has_default:
                    default_value = argument.default
                    default_type = ConverterDefaultType.object
                else:
                    default_value = None
                    default_type = ConverterDefaultType.none
                
                default_value, default_type = meta.validate_default(default_value, default_type)

                converter = object.__new__(Converter)
                converter.args = False
                converter.amount = 1
                converter.default_type = default_type
                converter.default_value = default_value
                converter.flags = meta.flags_default
                converter.meta = meta
        
            elif isinstance(annotation,str):
                if type(annotation) is not str:
                    annotation=str(annotation)
                
                try:
                    meta = ParserMeta.INSTANCES[annotation]
                except KeyError:
                    raise ValueError(f'Not passed callable would user a not supported type: `{annotation!r}`.') from None
                
                if argument.has_default:
                    default_value = argument.default
                    default_type = ConverterDefaultType.object
                else:
                    default_value = None
                    default_type = ConverterDefaultType.none
                
                default_value, default_type = meta.validate_default(default_value, default_type)
                
                converter = object.__new__(Converter)
                converter.args = False
                converter.amount = 1
                converter.default_type = default_type
                converter.default_value = default_value
                converter.flags = meta.flags_default
                converter.meta = meta
            
            elif type(annotation) is Converter:
                converter = annotation
                if argument.has_default:
                    converter.set_default(argument.default)
            
            else:
                raise ValueError(f'Annotation has unexpected annotation value: `{annotation!r}`.')
            
            if index==limit:
                converter.set_args()
        else:
            if index==limit:
                converter = Converter.args_str
            elif index==1 and limit==2:
                converter = Converter.content
            elif index==limit-1:
                converter = Converter.rest
            else:
                converter = Converter.str
        
        parsed_arguments.append(converter)
    
    if len(parsed_arguments) == 0:
        if should_instance:
            func = analyzer.instance_to_async_callable()
        return func, COMMAND_CALL_SETTING_2ARGS, None
    
    if len(parsed_arguments) == 1 and parsed_arguments[0]==Converter.content:
        if should_instance:
            func = analyzer.instance_to_async_callable()
        return func, COMMAND_CALL_SETTING_3ARGS, None
    
    parsed_arguments=tuple(parsed_arguments)
    
    try:
        parser = COMPILED_PARSERS[parsed_arguments]
    except KeyError:
        parser = compile_parsed(parsed_arguments)
        COMPILED_PARSERS[parsed_arguments] = parser
        
    return func, COMMAND_CALL_SETTING_USE_PARSER, parser


def compile_parsed(converters):
    result=code()
    
    for converter in converters:
        if converter.flags.guild:
            is_guild_only = True
            break
    else:
        is_guild_only = False
    
    if is_guild_only:
        needs_guild_set=True
    else:
        for converter in converters:
            flags=converter.flags
            if flags.id:
                needs_guild_set = True
                break
                
            if flags.name:
                needs_guild_set = True
                break
        else:
            needs_guild_set = False
    
    result.append(f'async def parser(client,message,content):')
    result.go_in()
    
    _locals=_unindexed_static.copy()
    counters={}
    
    result.append('result=[]')
    
    if needs_guild_set:
        result.append('guild=message.guild')
        _locals['guild']=_unindexed_optional['guild']
    
    if is_guild_only:
        result.append('if guild is None:')
        result.append('    return False,result')
    
    is_part_fallback_set=False
    is_part_set=False
    is_index_set=False
    for index in range(len(converters)):
        element=converters[index]
        name=element.meta.name
        
        if name=='condition':
            
            if element.default_type is not ConverterDefaultType.none:
                element.check_default(_locals)
                result.append(f'if {element.default_value}:')
                if element.flags.reversed:
                    result.extend('    return False,result')
                else:
                    result.append('    return True,result')
            else:
                pass #no default
            
            continue
        
        if name=='guild':
            #TODO : add support for guild parsing
            result.append('result.append(guild)')
            #no else case, guild can be used just for a placeholder for guild only commands
            continue
        
        if name=='rest':
            if is_index_set:
                if is_part_fallback_set:
                    result.append( 'if free_part:')
                    result.go_in()
                    result.append( 'if index:')
                    result.append( '    if index==limit:')
                    result.append( '        rest=part')
                    result.append( '    else:')
                    result.append( '        index_=parsed.start()')
                    result.append( '        if index_:')
                    result.append( '            rest=content[index_:]')
                    result.append( '        else:')
                    result.append( '            rest=content')
                    result.append( 'else:')
                    result.append( '    rest=content')
                    result.go_out()
                    result.append( 'else:')
                    result.go_in()

                result.append( 'if index:')
                result.append( '    if index==limit:')
                result.go_in(2)
                if element.default_type is ConverterDefaultType.none:
                    result.append( 'rest=\'\'')
                else:
                    element.check_default(_locals)
                    result.append(f'rest={element.default_value}')
                
                result.go_out(2)
                result.append( '    else:')
                result.append( '        rest=content[index:]')
                result.append( 'else:')
                result.append( '    rest=content')

            else:
                if element.default_type is ConverterDefaultType.none:
                    result.append( 'rest=content')
                else:
                    element.check_default(_locals)
                    result.append( 'if content:')
                    result.append( '    rest=content')
                    result.append( 'else:')
                    result.append(f'    rest={element.default_value}')
            
            result._back_state=1
            _locals[name]=_unindexed_optional[name]
            result.append(f'result.append({name})')
            continue
        
        if name=='message':
            #total ignore, we pass it by default
            continue
        
        if name=='content':
            if element.default_type is not ConverterDefaultType.none:
                result.append( 'if not content')
                element.check_default(_locals)
                result.append(f'    content={element.default_value}')
            
            result.append('result.append(content)')
            continue
        
        if (not is_index_set) and (index!=len(converters)-1 or (not element.parse_one)):
            is_index_set=True
            result.append('index=0')
            result.append('limit=len(content)')
        
        
        if name=='ensure':
            if not is_part_set:
                go_to=result._back_state
                if is_part_fallback_set:
                    result.append( 'if free_part:')
                    result.append( '    free_part=False')
                    result.append( 'else:')
                    result.go_in()
                if is_index_set:
                    result.append( 'if index==limit:')
                else:
                    result.append( 'if not content:')
                result.go_in()
                if element.default_type is ConverterDefaultType.none:
                    result.append( 'part=\'\'')
                else:
                    element.check_default(_locals)
                    result.append(f'part={element.default_value}')
                
                result.go_out()
                result.append( 'else:')
                result.go_in()
                if is_index_set:
                    result.append( 'parsed=PARSER_RP.match(content,index)')
                else:
                    result.append( 'parsed=PARSER_RP.match(content)')
                result.append( 'part=parsed.group(2)')
                result.append( 'if part is None:')
                result.append( '    part=parsed.group(1)')
                if index!=len(converters)-1:
                    result.append( 'index=parsed.end()')
                result._back_state=go_to
                _locals['part']=_unindexed_optional['part']
            is_part_set=True
            is_part_fallback_set=True
            continue


        counter=counters.get(name,0)
        counters[name]=counter+1
        variable_name=f'{name}_{counter}'
        
        
        if element.parse_one:
            loop=False
            sub_var_name=variable_name
        else:
            loop=True
            
            sub_var_name=name
            if not element.args:
                result.append(f'{variable_name}=[]')
                result.append(f'result.append({variable_name})')
            result.append( 'index_=0')
            if element.upper_limit:
                result.append(f'while index_<{element.upper_limit}:')
            else:
                result.append( 'while True:')
            result.go_in()
        
        if loop:
            if element.lower_limit:
                if element.default_type is ConverterDefaultType.none:
                    return_part_on_fail=[f'if index_<{element.lower_limit}:']
                    return_part_on_fail.append('    return False,result')
                else:
                    return_part_on_fail = [
                        f'default={element.default_value}',
                        f'while index_<{element.lower_limit}:',
                            ]
                    
                    if element.args:
                        return_part_on_fail.append(f'    result.append(default)')
                    else:
                        return_part_on_fail.append(f'    {variable_name}.append(default)')
                    
                    return_part_on_fail.append( '    index_+=1')
                    return_part_on_fail.append( 'break')
                
                return_part_on_fail_noneset=[f'if {sub_var_name} is None:']
                for line in return_part_on_fail:
                    return_part_on_fail_noneset.append('    '+line)
                if element.default_type is ConverterDefaultType.none:
                    return_part_on_fail_noneset.append('    break')
            else:
                return_part_on_fail=['break']
                return_part_on_fail_noneset=[
                    f'if {sub_var_name} is None:',
                     '    break']
            return_part_on_fail_nonset=return_part_on_fail
        elif element.default_type is not ConverterDefaultType.none:
            element.check_default(_locals)
            return_part_on_fail=[f'{sub_var_name}={element.default_value}']
            if element.default_value=='None':
                if index!=len(converters)-1:
                    return_part_on_fail_noneset=[f'free_part=({sub_var_name} is None)']
                else:
                    return_part_on_fail_noneset=[]
            else:
                if index!=len(converters)-1:
                    return_part_on_fail.append('free_part=True')
                    return_part_on_fail_noneset=[
                        f'if {sub_var_name} is None:',
                        f'    {sub_var_name}={element.default_value}',
                         '    free_part=True',]
                else:
                    return_part_on_fail_noneset=[
                        f'if {sub_var_name} is None:',
                        f'    {sub_var_name}={element.default_value}',]
                
            return_part_on_fail_nonset=[f'{sub_var_name}={element.default_value}',]
        
        else:
            return_part_on_fail=[
                 'return False,result',
                    ]
            return_part_on_fail_noneset=[
                f'if {sub_var_name} is None:',
                 '    return False,result',
                    ]
            
            return_part_on_fail_nonset=return_part_on_fail

        if not is_part_set:
            go_to=result._back_state
            if is_part_fallback_set:
                go_to+=1
            if is_index_set:
                if index!=len(converters)-1 and element.default_type is not ConverterDefaultType.none:
                    result.append( 'free_part=False')
                if is_part_fallback_set:
                    result.append( 'if index==limit and not free_part:')
                else:
                    result.append( 'if index==limit:')
            else:
                result.append( 'if not content:')
            result.extend(return_part_on_fail_nonset,1)
            result.append( 'else:')
            result.go_in()
            if is_part_fallback_set:
                result.append( 'if free_part:')
                result.append( '    free_part=False')
                result.append( 'else:')
                result.go_in()
            if is_index_set:
                result.append( 'parsed=PARSER_RP.match(content,index)')
            else:
                result.append( 'parsed=PARSER_RP.match(content)')
            result.append( 'part=parsed.group(2)')
            result.append( 'if part is None:')
            result.append( '    part=parsed.group(1)')
            if index!=len(converters)-1 or loop:
                result.append( 'index=parsed.end()')
            result._back_state=go_to+1
            _locals['part']=_unindexed_optional['part']
            if is_part_fallback_set:
                result.go_out()
        _locals[sub_var_name]=_indexed_optional[name]

        if (element.default_type is not ConverterDefaultType.none):
            is_part_fallback_set=True
            
        if name=='user':
            go_to=result._back_state
            if element.flags.name:
                if is_guild_only:
                    if CACHE_USER:
                        by_name_part = [
                             'if len(guild.users)>REQUEST_OVER:',
                            f'    found = await client.request_member(guild,part)',
                             '    if found:',
                            f'        {sub_var_name}=found[0]',
                             '    else:',
                            f'        {sub_var_name}=None',
                             'else:',
                            f'    {sub_var_name}=guild.get_user_like(part)',
                                ]
                    else:
                        by_name_part = [
                            f'found = await client.request_member(guild,part)',
                             'if found:',
                            f'    {sub_var_name}=found[0]',
                             'else:',
                            f'    {sub_var_name}=None',
                                ]
                else:
                    if CACHE_USER:
                        by_name_part = [
                             'if guild is None:',
                            f'    {sub_var_name}=message.channel.get_user_like(part)',
                             'else:',
                             '    if len(guild.users)>REQUEST_OVER:',
                            f'        found = await client.request_member(guild,part)',
                             '        if found:',
                            f'            {sub_var_name}=found[0]',
                             '        else:',
                            f'            {sub_var_name}=None',
                             '    else:',
                            f'        {sub_var_name}=guild.get_user_like(part)',
                                 ]
                    else:
                        by_name_part = [
                             'if guild is None:',
                            f'    {sub_var_name}=message.channel.get_user_like(part)',
                             'else:',
                            f'    found = await client.request_member(guild,part)',
                             '    if found:',
                            f'        {sub_var_name}=found[0]',
                             '    else:',
                            f'        {sub_var_name}=None',
                                 ]
            else:
                by_name_part=None
            
            if element.flags.mention:
                result.append(f'{sub_var_name}=parse_user_mention(part,message)')
                
                if element.flags.name or element.flags.everywhere or element.flags.id:
                    result.append(f'if {sub_var_name} is None:')
                    result.go_in()
            
            if element.flags.everywhere or element.flags.id:
                result.append( 'parsed_=IS_ID_RP.fullmatch(part)')
                result.append( 'if parsed_ is None:')
                result.go_in()
                result.extend(by_name_part)
                result.go_out()
                result.append( 'else:')
                result.go_in()
                result.append( 'id_=int(parsed_.group(1))')
                if element.flags.everywhere:
                    if (not CACHE_USER) and element.flags.profile:
                        if not is_guild_only:
                            result.append( 'if guild is None:')
                            result.go_in()
                            result.append( 'try:')
                            result.append(f'    {sub_var_name} = await client.user_get(id_)')
                            result.append( 'except DiscordException:')
                            result.append(f'    {sub_var_name}=None')
                            result.go_out()
                            result.append('else:')
                            result.go_in()
                        result.append( 'try:')
                        result.append(f'    {sub_var_name} = await client.guild_user_get(guild,id_)')
                        result.append( 'except DiscordException:')
                    else:
                        result.append( 'try:')
                        result.append(f'    {sub_var_name}=USERS[id_]')
                        result.append( 'except KeyError:')
                    result.go_in()
                    result.append( 'try:')
                    result.append(f'    {sub_var_name} = await client.user_get(id_)')
                    result.append( 'except DiscordException:')
                    result.append(f'    {sub_var_name}=None')
                    
                else:
                    if is_guild_only:
                        if (not CACHE_USER):
                            if element.flags.profile:
                                result.append('try:')
                                result.append(f'    {sub_var_name} = await client.guild_user_get(guild,id_)')
                                result.append('except DiscordException:')
                                result.append(f'    {sub_var_name}=None')
                        else:
                            result.append(f'{sub_var_name}=guild.users.get(id_)')
                    else:
                        result.append( 'if guild is None:')
                        result.go_in()
                        result.append(f'for {sub_var_name} in message.channel.users:')
                        result.append(f'    if {sub_var_name}.id==id_:')
                        result.append( '        break')
                        result.append( 'else:')
                        result.append(f'    {sub_var_name}=None')
                        result.go_out()
                        result.append('else:')
                        result.go_in()
                        if CACHE_USER:
                            result.append(f'{sub_var_name}=guild.users.get(id_)')
                        else:
                            if element.flags.profile:
                                result.append('try:')
                                result.append(f'    {sub_var_name} = await client.guild_user_get(guild,id_)')
                                result.append('except DiscordException:')
                                result.append(f'    {sub_var_name}=None')
                            else:
                                result.extend(return_part_on_fail_noneset)
            else:
                if element.flags.name:
                    result.extend(by_name_part)
            
            result._back_state=go_to
            result.extend(return_part_on_fail_noneset)
        
        elif name=='channel':
            go_to=result._back_state
            if element.flags.mention:
                result.append(f'{sub_var_name}=parse_channel_mention(part,message)')
                
                if element.flags.id or element.flags.name:
                    if not loop:
                        go_to+=1
                    result.append(f'if {sub_var_name} is None:')
                    result.go_in()

            if element.flags.id:
                result.append( 'parsed_=IS_ID_RP.fullmatch(part)')
                result.append( 'if parsed_ is not None:')
                result.go_in()
                result.append( 'id_=int(parsed_.group(1))')
                result.append(f'{sub_var_name}=guild.all_channel.get(id_)')
                if element.flags.name:
                    result.append(f'if {sub_var_name} is None:')
                    result.append(f'    {sub_var_name}=guild.get_channel_like(part)')
                    result.go_out()
                    result.append( 'else:')
                    result.append(f'    {sub_var_name}=guild.get_channel_like(part)')
            
            else:
                if element.flags.name:
                    result.append(f'{sub_var_name}=guild.get_channel_like(part)')
                    
            result._back_state=go_to
            result.extend(return_part_on_fail_noneset)

        elif name=='role':
            go_to=result._back_state
            if element.flags.mention:
                result.append(f'{sub_var_name}=parse_role_mention(part,message)')
                
                if element.flags.id or element.flags.name:
                    if not loop:
                        go_to+=1
                    result.append(f'if {sub_var_name} is None:')
                    result.go_in()
                    
            if element.flags.id:
                result.append( 'parsed_=IS_ID_RP.fullmatch(part)')
                result.append( 'if parsed_ is not None:')
                result.go_in()
                result.append( 'id_=int(parsed_.group(1))')
                result.append(f'{sub_var_name}=guild.all_role.get(id_)')
                if element.flags.name:
                    result.append(f'if {sub_var_name} is None:')
                    result.append(f'    {sub_var_name}=guild.get_role_like(part)')
                    result.go_out()
                    result.append( 'else:')
                    result.append(f'    {sub_var_name}=guild.get_role_like(part)')
            
            else:
                if element.flags.name:
                    result.append(f'{sub_var_name}=guild.get_role_like(part)')
                    
            result._back_state=go_to
            result.extend(return_part_on_fail_noneset)

        elif name=='emoji':
            go_to=result._back_state
            if element.flags.mention:
                result.append(f'{sub_var_name}=parse_emoji(part)')
                if element.flags.id or element.flags.everyhere or element.flags.name:
                    if not loop:
                        go_to+=1
                    result.append(f'if {sub_var_name} is None:')
                    result.go_in()
            
            if element.flags.id or element.flags.everywhere:
                if not element.flags.everywhere:
                    if not is_guild_only:
                        result.append( 'if guild is not None:')
                        result.go_in()
                        
                result.append( 'parsed_=IS_ID_RP.fullmatch(part)')
                result.append( 'if parsed_ is not None:')
                result.go_in()
                result.append( 'id_=int(parsed_.group(1))')
                if not element.flags.everywhere:
                    result.append(f'{sub_var_name}=guild.emojis.get(id_)')
                    if element.flags.name:
                        result.append(f'if {sub_var_name} is None:')
                        result.append(f'    {sub_var_name}=guild.get_emoji_like(part)')
                        result.go_out()
                        result.append( 'else:')
                        result.append(f'    {sub_var_name}=guild.get_emoji_like(part)')
                
                else:
                    result.append(f'{sub_var_name}=EMOJIS.get(id_)')
                    if element.flags.name:
                        result.append(f'if {sub_var_name} is None and guild is not None:')
                        result.append(f'    {sub_var_name}=guild.get_emoji_like(part)')
                        result.go_out()
                        result.append( 'else:')
                        result.go_in()
                        result.append('if guild is not None:')
                        result.append(f'    {sub_var_name}=guild.get_emoji_like(part)')
                
            else:
                if element.flags.name:
                    if not is_guild_only:
                        result.append( 'if guild is not None:')
                        result.go_in()
                    result.append(f'{sub_var_name}=guild.get_emoji_like(part)')
            
            result._back_state=go_to
            result.extend(return_part_on_fail_noneset)
            
        elif name=='str':
            result.append(f'{sub_var_name}=part')
            
        elif name=='int':
            result.append('if len(part)>INT_CONVERSION_LIMIT:')
            result.extend(return_part_on_fail,1)
            result.append('else:')
            result.go_in()
            result.append( 'try:')
            result.append(f'    {sub_var_name}=int(part)')
            result.append( 'except ValueError:')
            result.go_in()
            result.extend(return_part_on_fail)
            _locals[sub_var_name]=_indexed_optional['int']

        elif name=='tdelta' or (name=='rdelta' and (relativedelta is not None)):
            result.append(f'{sub_var_name}=parse_{name}(part)')
            result.extend(return_part_on_fail_noneset)
        else:
            raise RuntimeError(name)
        
        if loop:
            if element.args:
                result.append(f'result.append({sub_var_name})')
            else:
                result.append(f'{variable_name}.append({sub_var_name})')
            result._back_state=2
            if element.lower_limit or element.upper_limit:
                result.append( 'index_+=1')
            result._back_state=1
        else:
            result._back_state=1
            result.append(f'result.append({sub_var_name})')
        
        is_part_set=False
    
    result.append('return True,result')
    
    return result.compile(__file__,_globals,'parser')


class ContentParser(object):
    __slots__ = ('__func__', '_call_setting', '_is_method', '_parser', '_parser_failure_handler', )
    __wrapper__ = 1
    __async_call__= True
    
    def __new__(cls, func=None, parser_failure_handler=None, is_method=False):
        
        if (parser_failure_handler is not None):
            if is_method:
                parser_failure_handler = check_argcount_and_convert(parser_failure_handler, 5,
                    '`parser_failure_handler` expected 5 arguemnts if `is_method` is set to `True` (client, message, parent, content, args).')
            else:
                parser_failure_handler = check_argcount_and_convert(parser_failure_handler, 4,
                    '`parser_failure_handler` expected 4 arguemnts (client, message, content, args).')
        
        if func is None:
            return cls._wrapper(parser_failure_handler, is_method)
        
        if is_method:
            func = method(func, object())
        
        func, call_setting, parser = parse(func)
        
        if is_method:
            func = func.__func__
        
        self = object.__new__(cls)
        self.__func__       = func
        self._call_setting  = call_setting
        self._parser        = parser
        self._parser_failure_handler=parser_failure_handler
        self._is_method     = is_method
        return self
    
    class _wrapper(object):
        __slots__ = ('_is_method', '_parser_failure_handler', )
        def __init__(self, parser_failure_handler, is_method):
            self._parser_failure_handler=parser_failure_handler
            self._is_method = is_method
        
        def __call__(self, func):
            return ContentParser(func=func, parser_failure_handler=self._parser_failure_handler, is_method=self._is_method)
    
    async def __call__(self, client, message, content=''):
        call_setting = self._call_setting
        if call_setting == COMMAND_CALL_SETTING_USE_PARSER:
            passed, args = await self._parser(client, message, content)
            if not passed:
                parser_failure_handler = self._parser_failure_handler
                if parser_failure_handler is None:
                    return None
                
                return await parser_failure_handler(client, message, content, args)
            
            return await self.__func__(client, message, *args)
        
        if call_setting == COMMAND_CALL_SETTING_2ARGS:
            return await self.__func__(client, message)
        
        # last case: COMMAND_CALL_SETTING_3ARGS
        return await self.__func__(client, message, content)
    
    def __get__(self,obj,type_):
        if self._is_method:
            if (obj is None):
                return ContentParserMethod(self,type_)
            else:
                return ContentParserMethod(self,obj)
        
        return self

    def __set__(self,obj,value):
        raise AttributeError('can\'t set attribute')

    def __delete__(self,obj):
        raise AttributeError('can\'t delete attribute')
    
    @property
    def __doc__(self):
        return getattr(self.__func__,'__doc__',None)

class ContentParserMethod(MethodLike):
    __slots__ = ('__parent__', '__self__', )
    __reserved_argcount__ = 2
    __async_call__ = True
    
    def __new__(cls, content_parser, obj):
        self = object.__new__(cls)
        self.__parent__ = content_parser
        self.__self__   = obj
        return self
    
    @property
    def __func__(self):
        parent = self.parent
        parser = parent._parser
        if parser is None:
            return parent.__func__
        else:
            return parser
    
    async def __call__(self, client, message, content=''):
        parent = self.__self__
        content_parser = self.__parent__
        
        call_setting = content_parser._call_setting
        if call_setting == COMMAND_CALL_SETTING_USE_PARSER:
            passed, args = await content_parser._parser(client, message, content)
            if not passed:
                parser_failure_handler = content_parser._parser_failure_handler
                if parser_failure_handler is None:
                    return None
                
                return await parser_failure_handler(client, message, parent, content, args)
            
            return await content_parser.__func__(parent, client, message, *args)
        
        if call_setting == COMMAND_CALL_SETTING_2ARGS:
            return await content_parser.__func__(parent, client, message)
        
        # last case: COMMAND_CALL_SETTING_3ARGS
        return await content_parser.__func__(parent, client, message, content)
    
    @property
    def __module__(self):
        return self.__self__.__module__
    
    def __getattr__(self,name):
        parent = self.parent
        func = parent._parser
        if func is None:
            func = parent.__func__
        
        return getattr(func, name)

del re
del FlagBase
