# -*- coding: utf-8 -*-
#TODO: ask python for GOTO already
import re

from .dereaddons_local import code, function, method, any_to_any, modulize, \
    MethodLike
from .parsers import check_coro, EventDescriptor, check_name, just_convert


#for globals at compiling
try:
    from dateutil.relativedelta import relativedelta
except ImportError:
    relativedelta = None

from datetime import timedelta
from .others import USER_MENTION_RP, ROLE_MENTION_RP, CHANNEL_MENTION_RP,   \
    IS_ID_RP

from .user import USERS
from .exceptions import DiscordException
from .emoji import parse_emoji
from .client_core import CACHE_USER
from .parsers import DEFAULT_EVENT

#for types at eval testing
from . import client

async def defaultcoro():
    return

DELTA_RP=re.compile('([\+\-]?\d+) *([a-zA-Z]+)')
PARSER_RP=re.compile('(?:"(.+?)"|(\S+))[^"\S]*')
MODE_RP=re.compile('(\*?)(\d*)([\+\-]?)(\d*)(\*?)')

del re


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
        

_globals = {
    'USERS'                 : USERS,
    'parse_user_mention'    : parse_user_mention,
    'parse_role_mention'    : parse_role_mention,
    'parse_channel_mention' : parse_channel_mention,
    'defaultcoro'           : defaultcoro,
    'DiscordException'      : DiscordException,
    'parse_emoji'           : parse_emoji,
    'parse_tdelta'          : parse_tdelta,
    'PARSER_RP'             : PARSER_RP,
    'IS_ID_RP'              : IS_ID_RP,
        }

if (relativedelta is not None):
    _globals['parse_rdelta']=parse_rdelta

_indexed_optional = {
    'user'      : _eval_tester_cls((client.User,client.Client,client.Webhook,client.UserOA2,),'user'),
    'role'      : _eval_tester_cls(client.Role,'role'),
    'channel'   : _eval_tester_cls(tuple(client.CHANNEL_TYPES),'channel'),
    'emoji'     : _eval_tester_cls(client.Emoji,'emoji'),
    'str'       : _eval_tester_cls(str,'str'),
    'int'       : _eval_tester_cls(int,'int'),
    'tdelta'    : _eval_tester_cls(timedelta,'tdelta'),
        }

if (relativedelta is not None):
    _indexed_optional['rdelta']=_eval_tester_cls(relativedelta,'rdelta')

_unindexed_static = {
    'client'    : _eval_tester_cls(client.Client,'client'),
    'message'   : _eval_tester_cls(client.Message,'message'),
    'content'   : _eval_tester_cls(str,'content'),
    'index'     : _eval_tester_cls(int,'index'),
    'limit'     : _eval_tester_cls(int,'limit'),
        }

_unindexed_optional = {
    'part'      : _eval_tester_cls(str,'part'),
    'guild'     : _eval_tester_cls(client.Guild,'guild'),
    'rest'      : _eval_tester_cls(str,'rest'),
        }

del USERS, defaultcoro, DiscordException, parse_emoji, IS_ID_RP, client

class ParserMeta(object):
    INSTANCES = {}
    
    __slots__=('name', 'flags_must', 'flags_default', 'flags_all',
        'passing_enabled', 'mode_enabled', 'default_enabled', 'default_must',)
    
    def __init__(self,name,flags_must,flags_default,flags_all,passing_enabled,mode_enabled,default_enabled,default_must):
        self.INSTANCES[name]= self
        self.name           = name
        self.flags_must     = [*flags_must]
        self.flags_default  = flags_default
        self.flags_all      = flags_all
        self.passing_enabled= passing_enabled,
        self.mode_enabled   = mode_enabled
        self.default_enabled= default_enabled
        self.default_must   = default_must

    def validate_flags(self,value):
        result=self.flags_must.copy()
        for char in value:
            if char not in self.flags_all:
                continue
            if char in result:
                continue
            result.append(char)
        if result==self.flags_must:
            return self.flags_default
        return ''.join(result)

    def validate_passit(self,value):
        if self.passing_enabled:
            return value
        return False

    def validate_mode(self,value):
        if not self.mode_enabled:
            value=''

        if not value:
            return (0,1,1)

        parsed=MODE_RP.fullmatch(value)
        if parsed is None:
            raise SyntaxError(f'could not parse mode : {value}') #oof

        s1,n1,op,n2,s2=parsed.groups()
        star=len(s1)|len(s2) #ignore dupe
        if n1:
            v1=int(n1)
        else:
            v1=0
        if n2:
            v2=int(n2)
        else:
            v2=0

        if op=='+' and v1 and v2: #make sure
            raise SyntaxError('If 2 values is set, cannot set operation to \'+\'')

        if star and not (v1 or v2): #make sure
            raise SyntaxError('If 0 values is set, cannot set star')

        if op=='+':
            if v2:
                v1=v2
                v2=0
        elif v1!=0 and v2!=0 and v1>v2:
            v2,v1=v1,v2

        return (star,v1,v2)

    def validate_default(self,value):
        if self.default_enabled:
            if self.default_must and not value:
                raise ValueError('For {self.name} \'default\' should have been passed')
            return value
        return ''

#          name         flags_name  flags_default   flags_all       passing_enabled mode_enabled    default_enabled default_must
ParserMeta('user',      '',         'mni',          'gmniap',       True,           True,           True,           False,          )
ParserMeta('role',      'g',        'gmni',         'gmni',         True,           True,           True,           False,          )
ParserMeta('channel',   'g',        'gmni',         'gmni',         True,           True,           True,           False,          )
ParserMeta('guild',     'g',        'g',            'g',            True,           False,          False,          False,          )
ParserMeta('message',   '',         '',             'g',            False,          False,          False,          False,          )
ParserMeta('emoji',     '',         '',             'g',            True,           True,           True,           False,          )
ParserMeta('content',   '',         '',             'g',            True,           False,          True,           False,          )
ParserMeta('rest',      '',         '',             'g',            True,           False,          True,           False,          )
ParserMeta('condition', '',         '',             'gr',           True,           False,          True,           True,           )
ParserMeta('str',       '',         '',             'g',            True,           True,           True,           False,          )
ParserMeta('int',       '',         '',             'g',            True,           True,           True,           False,          )
ParserMeta('ensure',    '',         '',             'g',            True,           False,          True,           False,          )
ParserMeta('tdelta',    '',         '',             'g',            True,           True,           True,           False,          )

if (relativedelta is not None):
    ParserMeta('rdelta','',         '',             'g',            True,           True,           True,           False,          )


class parsed_line(object):
    __slots__=('meta', 'default', 'flags', 'name', 'mode', 'passit',)
    def __init__(self,name,kwargs):
        try:
            self.meta=ParserMeta.INSTANCES[name]
        except KeyError:
            raise ValueError(f'There is nothing defined to deal with {name!r}') from None
        self.name=name
        self.fillup(kwargs)
        
    def fillup(self,kwargs):
        meta=self.meta
        self.passit=meta.validate_passit(kwargs.pop('passit',True))
        self.default=meta.validate_default(kwargs.pop('default',''))
        self.flags=meta.validate_flags(kwargs.pop('flags',''))
        self.mode=meta.validate_mode(kwargs.pop('mode',''))

        if kwargs:
            raise TypeError('fillup got an unexpected keyword arguments : {", ".join(list(kwargs))}')

    def check_default(self,_locals):
        try:
            eval(self.default,_globals,_locals)
        except AttributeError as err:
            args=err.args
            if len(args)==2:
                err.args=(f'type {args[0]} has no attribute \'{args[1]}\'.',)
            raise
        except NameError:
            raise
        except Exception:
            pass

    @property
    def pass_as_list(self):
        return self.mode[0]

    @property
    def parse_one(self):
        mode=self.mode
        return 1==mode[1]==mode[2]

    @property
    def is_exactly(self):
        mode=self.mode
        return mode[1]==mode[2]

    @property
    def lower_limit(self):
        return self.mode[1]

    @property
    def upper_limit(self):
        return self.mode[2]

    @staticmethod
    def _parse_space(text,index,limit):
        while True:
            if index==limit:
                return index
            char=ord(text[index])
            if char in (9,10,13,32,): #'\t\n\r '
                index=index+1
                continue
            return index
                  

    @staticmethod
    def _parse_keyword(text,index,limit):
        actual=[]
        while True:
            if index==limit:
                break
            char=ord(text[index])
            if char<49:
                if char in (10,13,32,44):
                    break
                raise SyntaxError(f'{text!r} at {index}')
            elif char<58: #49-57 is 0-9
                actual.append(char)
            elif char<65: #65-90 is A-Z
                if char==61:
                    break
                raise SyntaxError(f'{text!r} at {index}')
            elif char<91:
                actual.append(char)
            elif char<97: #97-122 is a-z
                if char==95: #95 is _
                    actual.append(char)
                raise SyntaxError(f'{text!r} at {index}')
            elif char<123:
                actual.append(char)
            else:
                raise SyntaxError(f'{text!r} at {index}')
            index=index+1
        return index,''.join([chr(char) for char in actual])
    
    @classmethod
    def _parse_char(cls,text,index,limit,char):
        index=cls._parse_space(text,index,limit)
        if index==limit:
            return index
        if text[index]!=char:
            raise SyntaxError(f'{text!r} at {index}')
        index=index+1
        index=cls._parse_space(text,index,limit)
        return index

    @staticmethod
    def _parse_str(text,index,limit):
        actual=[]
        if index==limit:
            return index,''
        starter=ord(text[index])
        if starter in (34,39):
            index=index+1
        else:
            starter=0
            
        in_dash=0
        
        while True:
            if index==limit:
                if starter:
                    raise SyntaxError(f'{text!r} at {index}')
                else:
                    return index,''.join([chr(char) for char in actual])
            char=ord(text[index])
            while True:
                if char==92:
                    if in_dash:
                        actual.append(92)
                        actual.append(92)
                    in_dash^=1
                    break
                
                if char in (34,39):
                    if in_dash:
                        actual.append(92)
                        in_dash=0
                    elif char==starter:
                        return index+1,''.join([chr(char) for char in actual])
                    actual.append(char)
                    break

                if not starter and char in (10,13,32,44):
                    if in_dash:
                        actual.append(92)
                    return index,''.join([chr(char) for char in actual])
                
                if in_dash:
                    in_dash=0
                    actual.append(92)
                actual.append(char)
                break
            
            index=index+1
            
    @classmethod
    def from_str(cls,text):
        limit=len(text)
        index=cls._parse_space(text,0,limit)
        index,name=cls._parse_keyword(text,index,limit)

        kwargs={}

        while index<limit:
            new_index=cls._parse_char(text,index,limit,',')
            if new_index==index:
                break
            index=new_index
            
            index,key=cls._parse_keyword(text,index,limit)

            if key in kwargs:
                raise ValueError('Multyple \'{valid_name}\' are passed')
                                 
            new_index=cls._parse_char(text,index,limit,'=')
            if new_index==index:
                raise SyntaxError(f'{text!r} at {index}')
            index=new_index

            index,value=cls._parse_str(text,index,limit)

            kwargs[key]=value
            
        return cls(name,kwargs)

    def __hash__(self):
        return hash(self.default)^hash(self.flags)^hash(self.name)^hash(self.mode)^(self.passit<<15)

COLLECTION={}
def get_parser(patterns,on_failure,is_method):
    parsed=content_parser_compiler.parse_pattern(patterns)
    if (on_failure is not None):
        fail_flag=('f','c')[check_coro(on_failure)]
        if parsed:
            line=parsed[0]
        else:
            line=(parsed_line('message',{}))
            parsed=(line,)
        line.flags+=fail_flag

    if is_method:
        if parsed:
            line=parsed[0]
        else:
            line=(parsed_line('message',{}))
            parsed=(line,)
        line.flags+='d'

    parser=COLLECTION.get(parsed,None)
    if parser is None:
        parser=content_parser_compiler.compile_parsed(parsed)
        COLLECTION[parsed]=parser
    return parser
    
@modulize
class content_parser_compiler:
    def parse_pattern(pattern):
        parsed=[]
        for element in pattern:
            if type(element) is parsed_line:
                parsed.append(element)
                continue
            if type(element) is str:
                parsed.append(parsed_line.from_str(element))
                continue

            raise TypeError(f'Pattern elements can be type str or parsed_line, got {element.__class__.__name__}')
        
        return tuple(parsed)

    def compile_parsed(parsed):
        result=code()

        is_method=any(('d' in x.flags) for x in parsed)
        is_guild_only=any(('g' in x.flags) for x in parsed)
        if is_guild_only:
            needs_guild_set=True
        else:
            needs_guild_set=any(any_to_any('ni',x.flags) for x in parsed)

        parsed_flag=0
        if parsed:
            if 'f' in parsed[0].flags:
                parsed_flag+=0b010
            elif 'c' in parsed[0].flags:
                parsed_flag+=0b100

        result.append(f'async def parser(self,{"parent," if is_method else ""}client,message,content):')
        result.go_in()
        
        _locals=_unindexed_static.copy()
        results=[]
        counters={}
        
        if needs_guild_set:
            result.append('guild=message.guild')
            _locals['guild']=_unindexed_optional['guild']
        if is_guild_only:
            result.append('if guild is None:')
            result.extend(content_parser_compiler._return_line_on_fail(parsed_flag,results,is_method),1)

        is_part_fallback_set=False
        is_part_set=False
        is_index_set=False
        for index in range(len(parsed)):
            element=parsed[index]
            case=element.name


            if case=='condition':
                
                if element.default:
                    element.check_default(_locals)
                    result.append(f'if {element.default}:')
                    if 'r' in element.flags:
                        result.extend(content_parser_compiler._return_line_on_fail(parsed_flag,results,is_method),1)
                    else:
                        result.append(content_parser_compiler._return_line_on_success(results,is_method),1)
                        
                else:
                    pass #no default
                continue

            if case=='guild':
                #TODO : add support for guild parsing
                if element.passit:
                    results.append('guild')
                #no else case, guild can be used just for a placeholder for guild only commands
                continue

            if case=='rest':
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
                    if element.default:
                        element.check_default(_locals)
                        result.append(f'rest={element.default}')
                    else:
                        result.append( 'rest=\'\'')
                    result.go_out(2)
                    result.append( '    else:')
                    result.append( '        rest=content[index:]')
                    result.append( 'else:')
                    result.append( '    rest=content')

                else:
                    if element.default:
                        element.check_default(_locals)
                        result.append( 'if content:')
                        result.append( '    rest=content')
                        result.append( 'else:')
                        result.append(f'    rest={element.default}')
                    else:
                        result.append( 'rest=content')

                result._back_state=1
                _locals[case]=_unindexed_optional[case]
                if element.passit:
                    results.append(case)
                continue

            if case=='message':
                #total ignore, we pass it by default
                continue

            if case=='content':
                if element.default:
                    result.append( 'if not content')
                    element.check_default(_locals)
                    result.append(f'    content={element.default}')
                if element.passit:
                    results.append('content')
                continue
                
            if (not is_index_set) and (index!=len(parsed)-1 or (not element.parse_one)):
                is_index_set=True
                result.append('index=0')
                result.append('limit=len(content)')


            if case=='ensure':
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
                    if element.default:
                        element.check_default(_locals)
                        result.append(f'part={element.default}')
                    else:
                        result.append( 'part=\'\'')
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
                    if index!=len(parsed)-1:
                        result.append( 'index=parsed.end()')
                    result._back_state=go_to
                    _locals['part']=_unindexed_optional['part']
                is_part_set=True
                is_part_fallback_set=True
                continue


            counter=counters.get(case,0)
            counters[case]=counter+1
            variable_name=f'{case}_{counter}'

            
            if element.parse_one:
                loop=False
                sub_var_name=variable_name
            else:
                loop=True

                if element.passit:
                    if element.pass_as_list:
                        results.append('*'+variable_name)
                    else:
                        results.append(variable_name)
                sub_var_name=case
                result.append(f'{variable_name}=[]')
                result.append( 'index_=0')
                if element.upper_limit:
                    result.append(f'while index_<{element.upper_limit}:')
                else:
                    result.append( 'while True:')
                result.go_in()

            if loop:
                if element.lower_limit:
                    if element.default:
                        return_part_on_fail=[
                            f'while index_<{element.lower_limit}:',
                            f'    {variable_name}.append({sub_var_name})',
                             '    index_+=1',
                             'break']
                    else:
                        return_part_on_fail=[f'if index_<{element.lower_limit}:']
                        for line in content_parser_compiler._return_line_on_fail(parsed_flag,results,is_method):
                            return_part_on_fail.append('    '+line)
                    
                    return_part_on_fail_noneset=[f'if {sub_var_name} is None:']
                    for line in return_part_on_fail:
                        return_part_on_fail_noneset.append('    '+line)
                    if not element.default:
                        return_part_on_fail_noneset.append('    break')
                else:
                    return_part_on_fail=['break']
                    return_part_on_fail_noneset=[
                        f'if {sub_var_name} is None:',
                         '    break']
                return_part_on_set=return_part_on_fail
            elif element.default:
                element.check_default(_locals)
                return_part_on_fail=[f'{sub_var_name}={element.default}']
                if element.default=='None':
                    if index!=len(parsed)-1:
                        return_part_on_fail_noneset=[f'free_part=({sub_var_name} is None)']
                        return_part_on_set=[ 'free_part=False']
                    else:
                        return_part_on_fail_noneset=[]
                        return_part_on_set=return_part_on_fail
                else:
                    if index!=len(parsed)-1:
                        return_part_on_fail.append('free_part=True')
                        return_part_on_fail_noneset=[
                            f'if {sub_var_name} is None:',
                            f'    {sub_var_name}={element.default}',
                             '    free_part=False',
                             'else:',
                             '    free_part=True',]
                        return_part_on_set=[
                            f'{sub_var_name}={element.default}',
                             'free_part=False']
                    else:
                        return_part_on_fail_noneset=[
                            f'if {sub_var_name} is None:',
                            f'    {sub_var_name}={element.default}',]
                        return_part_on_set=[f'{sub_var_name}={element.default}',]
                        
            else:
                return_part_on_fail=content_parser_compiler._return_line_on_fail(parsed_flag,results,is_method)
                return_part_on_fail_noneset=[f'if {sub_var_name} is None:']
                for line in return_part_on_fail:
                    return_part_on_fail_noneset.append('    '+line)
                return_part_on_set=return_part_on_fail

            if element.default and index!=len(parsed)-1:
                parsing_succes_part=['free_part=False']
            else:
                parsing_succes_part=[]

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
                result.extend(return_part_on_set,1)
                result.append( 'else:')
                result.go_in()
                if is_index_set:
                    result.append( 'parsed=PARSER_RP.match(content,index)')
                else:
                    result.append( 'parsed=PARSER_RP.match(content)')
                result.append( 'part=parsed.group(2)')
                result.append( 'if part is None:')
                result.append( '    part=parsed.group(1)')
                if index!=len(parsed)-1 or loop:
                    result.append( 'index=parsed.end()')
                result._back_state=go_to+1
                _locals['part']=_unindexed_optional['part']
                if is_part_fallback_set:
                    result.go_out()
            _locals[sub_var_name]=_indexed_optional[case]

            if element.default:
                is_part_fallback_set=True
                
            if case=='user':
                go_to=result._back_state
                if 'n' in element.flags:
                    if is_guild_only:
                        if CACHE_USER:
                            by_name_part = [
                                 'if len(guild.users)>self.REQUEST_OVER:',
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
                                 '    if len(guild.users)>self.REQUEST_OVER:',
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
                
                if 'm' in element.flags:
                    result.append(f'{sub_var_name}=parse_user_mention(part,message)')
                    
                    if any_to_any(('a','i','n',),element.flags):
                        result.append(f'if {sub_var_name} is None:')
                        result.go_in()

                if any_to_any(('a','i'),element.flags):
                    result.append( 'parsed_=IS_ID_RP.fullmatch(part)')
                    result.append( 'if parsed_ is None:')
                    result.go_in()
                    result.extend(by_name_part)
                    result.go_out()
                    result.append( 'else:')
                    result.go_in()
                    result.append( 'id_=int(parsed_.group(1))')
                    if 'a' in element.flags:
                        if (not CACHE_USER) and ('p' in element.flags):
                            if not is_guild_only:
                                result.append( 'if guild is None:')
                                result.go_in()
                                result.append( 'try:')
                                result.append(f'    {sub_var_name} = await client.user_get(id_)')
                                result.extend(parsing_succes_part,1)
                                result.append( 'except DiscordException:')
                                result.append(f'    {sub_var_name}=None')
                                result.go_out()
                                result.append('else:')
                                result.go_in()
                            result.append( 'try:')
                            result.append(f'    {sub_var_name} = await client.guild_user_get(guild,id_)')
                            result.extend(parsing_succes_part,1)
                            result.append( 'except DiscordException:')
                        else:
                            result.append( 'try:')
                            result.append(f'    {sub_var_name}=USERS[id_]')
                            result.extend(parsing_succes_part,1)
                            result.append( 'except KeyError:')
                        result.go_in()
                        result.append( 'try:')
                        result.append(f'    {sub_var_name} = await client.user_get(id_)')
                        result.extend(parsing_succes_part,1)
                        result.append( 'except DiscordException:')
                        result.append(f'    {sub_var_name}=None')
                        
                    else: #i
                        if is_guild_only:
                            if (not CACHE_USER):
                                if ('p' in element.flags):
                                    result.append('try:')
                                    result.append(f'    {sub_var_name} = await client.guild_user_get(guild,id_)')
                                    result.extend(parsing_succes_part,1)
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
                            if (not CACHE_USER):
                                if 'p' in element.flags:
                                    result.append('try:')
                                    result.append(f'    {sub_var_name} = await client.guild_user_get(guild,id_)')
                                    result.extend(parsing_succes_part,1)
                                    result.append('except DiscordException:')
                                    result.append(f'    {sub_var_name}=None')
                            else:
                                result.append(f'{sub_var_name}=guild.users.get(id_)')

                else:
                    if 'n' in element.flags:
                        result.extend(by_name_part)
                
                result._back_state=go_to
                result.extend(return_part_on_fail_noneset)
            
            elif case=='channel':
                go_to=result._back_state
                if 'm' in element.flags:
                    result.append(f'{sub_var_name}=parse_channel_mention(part,message)')
                    
                    if any_to_any(('i','n',),element.flags):
                        result.append(f'if {sub_var_name} is None:')
                        result.go_in()

                if 'i' in element.flags:
                    result.append( 'parsed_=IS_ID_RP.fullmatch(part)')
                    result.append( 'if parsed_ is not None:')
                    result.go_in()
                    result.append( 'id_=int(parsed_.group(1))')
                    result.append(f'{sub_var_name}=guild.all_channel.get(id_)')
                    result.go_out()
                    if 'n' in element.flags:
                        result.append( 'else:')
                        result.append(f'    {sub_var_name}=guild.get_channel(part)')
                
                else:
                    if 'n' in element.flags:
                        result.append(f'{sub_var_name}=guild.get_channel(part)')
                        
                result._back_state=go_to
                result.extend(return_part_on_fail_noneset)

            elif case=='role':
                go_to=result._back_state
                if 'm' in element.flags:
                    result.append(f'{sub_var_name}=parse_role_mention(part,message)')
                    
                    if any_to_any(('i','n',),element.flags):
                        result.append(f'if {sub_var_name} is None:')
                        result.go_in()
                        
                if 'i' in element.flags:
                    result.append( 'parsed_=IS_ID_RP.fullmatch(part)')
                    result.append( 'if parsed_ is not None:')
                    result.go_in()
                    result.append( 'id_=int(parsed_.group(1))')
                    result.append(f'{sub_var_name}=guild.all_role.get(id_)')
                    result.go_out()
                    if 'n' in element.flags:
                        result.append( 'else:')
                        result.append(f'    {sub_var_name}=guild.get_role(part)')
                
                else:
                    if 'n' in element.flags:
                        result.append(f'{sub_var_name}=guild.get_role(part)')
                        
                result._back_state=go_to
                result.extend(return_part_on_fail_noneset)

            elif case=='emoji':
                result.append(f'{sub_var_name}=parse_emoji(part)')
                result.extend(return_part_on_fail_noneset)
                
            elif case=='str':
                result.append(f'{sub_var_name}=part')
                result.extend(parsing_succes_part)
                
            elif case=='int':
                result.append('if len(part)>self.INT_CONVERSION_LIMIT:')
                result.extend(return_part_on_fail,1)
                result.append('else:')
                result.go_in()
                result.append( 'try:')
                result.append(f'    {sub_var_name}=int(part)')
                result.extend(parsing_succes_part,1)
                result.append( 'except ValueError:')
                result.go_in()
                result.extend(return_part_on_fail)
                _locals[sub_var_name]=_indexed_optional['int']

            elif case=='tdelta' or (case=='rdelta' and (relativedelta is not None)):
                result.append(f'{sub_var_name}=parse_{case}(part)')
                result.extend(return_part_on_fail_noneset)
            else:
                raise RuntimeError(case)
            
            if loop:
                result.append(f'{variable_name}.append({sub_var_name})')
                result._back_state=2
                if element.lower_limit or element.upper_limit:
                    result.append( 'index_+=1')
                
            result._back_state=1
            if element.passit and (not loop):
                results.append(variable_name)
            is_part_set=False

        result.append(content_parser_compiler._return_line_on_success(results,is_method))
        
        return result.compile(__file__,_globals,'parser')

    def _return_line_on_success(results,is_method):
        to_pass=','.join(results)
        return f'return await self.__func__({"parent," if is_method else ""}client,message,{to_pass})'
        
    def _return_line_on_fail(parsed_flag,results,is_method):
        if parsed_flag<2:
            return ['return']
        to_pass=','.join(results)
        if parsed_flag<4:
            return [f'return await self._on_failure({"parent," if is_method else ""}client,message,{to_pass})']
        if parsed_flag==4:
            return [f'return await self._on_failure({"parent," if is_method else ""}client,message,{to_pass})']


class ContentParserMethod(MethodLike):
    __slots__=('__parent__','__self__',)
    __reserved_argcount__=2
    __async_call__=True

    def __init__(self,content_parser,obj):
        self.__parent__ = content_parser
        self.__self__   = obj

    @property
    def __func__(self):
        return self.__parent__._parser

    def __call__(self,client,message,content):
        content_parser=self.__parent__
        return content_parser._parser(content_parser,self.__self__,client,message,content)

    @property
    def __code__(self):
        return self.__parent__._parser.__code__

    @property
    def __module__(self):
        return self.__self__.__module__

    @property
    def __name__(self):
        return self.__parent__.__func__.__name__


class ContentParser(object):
    __async_call__=True
    __slots__=('__func__', '__name__', '_on_failure', '_parser','_is_method')
    REQUEST_OVER=1000
    INT_CONVERSION_LIMIT=100
    def __new__(cls,*patterns,on_failure=None,case=None,is_method=False,func=None):
        if (func is not None) and (not check_coro(func)):
            raise TypeError(f'{cls.__name__} expected coroutine function, got {func!r}')

        self=object.__new__(cls)
        self._parser=get_parser(patterns,on_failure,is_method)
        self._on_failure=on_failure
        self._is_method=is_method

        if (case is not None) and (not case.islower()):
            case=case.lower()
        
        if func is None:
            self.__name__=case
            self.__func__=DEFAULT_EVENT
            return self._wrapper
        
        self.__name__=check_name(func,case)
        self.__func__=just_convert(func)
        return self

    def _wrapper(self,func):
        if (not check_coro(func)):
            raise TypeError(f'{self.__class__.__name__} expected coroutine function, got {func!r}')

        if not self.__name__:
            self.__name__=check_name(func,None)
        self.__func__=just_convert(func)
        return self
        
    def __call__(self,client,message,content):
        return self._parser(self,client,message,content)
    
    def __repr__(self):
        result=['<',self.__class__.__name__,' func=',repr(self.__func__)]
        
        on_failure=self._on_failure
        if on_failure is not None:
            result.append(', on_failure=')
            result.append(repr(on_failure))
        result.append('>')
        
        return ''.join(result)

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

del modulize
