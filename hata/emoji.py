# -*- coding: utf-8 -*-
__all__ = ('BUILTIN_EMOJIS', 'Emoji', 'parse_emoji', 'reaction_mapping',
    'reaction_mapping_line',)

from .client_core import EMOJIS
from .others import id_to_time, EMOJI_RP
from .http import URLS
from .user import User, ZEROUSER

from . import activity

UNICODE_EMOJI_LIMIT=0b10000000000000000000000

def PartialEmoji(data):
    emoji_id=data.get('id')
    if emoji_id is None:
        name=data['name']
        try:
            return UNICODE_TO_EMOJI[name]
        except KeyError:
            raise RuntimeError(f'Undefined emoji : {name.encode()!r}\nPlease open an issue with this message.') from None
    
    emoji_id=int(emoji_id)
    
    try:
        emoji=EMOJIS[emoji_id]
    except KeyError:
        emoji           = object.__new__(Emoji)
        emoji.id        = emoji_id
        emoji.animated  = data.get('animated',False)
        EMOJIS[emoji_id]= emoji
        emoji.unicode   = None
        emoji.guild     = None

    # name can change
    name=data['name']
    if name is None:
        name=''
    
    emoji.name=name
    
    return emoji
    
class Emoji(object):
    __slots__=('__weakref__', 'animated', 'available', 'guild', 'id',
        'managed', 'name', 'require_colons', 'roles', 'unicode', 'user',)
    
    def __new__(cls,data,guild):
        emoji_id=int(data['id'])

        try:
            emoji=EMOJIS[emoji_id]
        except KeyError:
            emoji=object.__new__(cls)
            emoji.id=emoji_id
            EMOJIS[emoji_id]=emoji
        else:
            # whenever we receive an emoji, it will have no user data included,
            # so it is enough if we check for user data only whenever we
            # receive emoji data from a request or so.
            if (emoji.guild is not None):
                if not emoji.user.id:
                    try:
                        user_data=data['user']
                    except KeyError:
                        pass
                    else:
                        emoji.user=User(user_data)
                return emoji
        
        name = data['name']
        if name is None:
            name=''
        
        emoji.name          = name
        emoji.animated      = data.get('animated',False)
        emoji.require_colons= data.get('require_colons',True)
        emoji.managed       = data.get('managed',False)
        emoji.guild         = guild
        emoji.available     = data.get('available',True)
        emoji.user          = ZEROUSER
        emoji.unicode       = None
        
        try:
            role_ids=data['roles']
        except KeyError:
            emoji.roles=None
        else:
            emoji.roles={guild.all_role[int(role_id)] for role_id in role_ids}
        
        return emoji

    def __gt__(self,other):
        if type(self) is type(self):
            return self.id>other.id
        return NotImplemented
        
    def __ge__(self,other):
        if type(self) is type(self):
            return self.id<other.id
        return NotImplemented
    
    def __eq__(self,other):
        if type(self) is type(self):
            return self.id==other.id
        return NotImplemented
        
    def __ne__(self,other):
        if type(self) is type(self):
            return self.id!=other.id
        return NotImplemented
    
    def __le__(self,other):
        if type(self) is type(self):
            return self.id<=other.id
        return NotImplemented
        
    def __lt__(self,other):
        if type(self) is type(self):
            return self.id<other.id
        return NotImplemented
    
    @classmethod
    def precreate(cls,emoji_id,**kwargs):
        try:
            emoji=EMOJIS[emoji_id]
        except KeyError:
            emoji=object.__new__(cls)

            if kwargs:
                emoji.name=kwargs.pop('name','')
                emoji.animated=kwargs.pop('animated',False)
                if kwargs:
                    for name,value in kwargs.items():
                        if name in ('id','guild','unicode','user'):
                            raise AttributeError(f'Cannot set {name!r} attribute with precreate!')
                        setattr(emoji,name,value)
            else:
                emoji.name=''
                emoji.animated=False

            emoji.id        = emoji_id 
            emoji.guild     = None
            emoji.unicode   = None
            emoji.user      = ZEROUSER
            
            EMOJIS[emoji_id]= emoji

        else:
            if emoji.guild is None and kwargs:
                for name,value in kwargs.items():
                    if name in ('id','guild','unicode','user'):
                        raise AttributeError(f'Cannot set {name!r} attribute with precreate!')
                    setattr(emoji,name,value)

        return emoji
    
    def __hash__(self):
        return self.id

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'<{self.__class__.__name__} id={self.id} name={self.name}>'

    def __format__(self,code):
        if not code:
            return self.name
        if code=='e':
            if self.id<UNICODE_EMOJI_LIMIT:
                return self.unicode
            if self.animated:
                return f'<a:{self.name}:{self.id}>'
            else:
                return f'<:{self.name}:{self.id}>'
        if code=='r':
            if self.id<UNICODE_EMOJI_LIMIT:
                return self.unicode
            return f'{self.name}:{self.id}'
        if code=='c':
            return f'{self.created_at:%Y.%m.%d-%H:%M:%S}'
        raise ValueError(f'Unknown format code {code!r} for object of type {self.__class__.__name__!r}')
    
    @property
    def partial(self):
        return (self.guild is None)
    
    def is_custom_emoji(self):
        return self.id>UNICODE_EMOJI_LIMIT

    def is_unicode_emoji(self):
        return self.id<UNICODE_EMOJI_LIMIT

    @property
    def as_reaction(self):
        if self.id<UNICODE_EMOJI_LIMIT:
            return self.unicode
        return f'{self.name}:{self.id}'

    @property
    def as_emoji(self):
        if self.id<UNICODE_EMOJI_LIMIT:
            return self.unicode
        if self.animated:
            return f'<a:{self.name}:{self.id}>'
        else:
            return f'<:{self.name}:{self.id}>'

    @property
    def created_at(self):
        return id_to_time(0 if self.id<UNICODE_EMOJI_LIMIT else self.id)

    url=property(URLS.emoji_url)
    url_as=URLS.emoji_url_as
    
    def _delete(self):
        del self.guild.emojis[self.id]
        self.roles = None
        self.guild = None
        self.available = False
        
    def _update_no_return(self,data):
        guild=self.guild
        
        self.require_colons=data.get('require_colons',True)
        self.managed=data.get('managed',False)
        
        self.animated=data.get('animated',False)
        
        name=data['name']
        if name is None:
            name=''
        
        self.name=name
        
        try:
            role_ids=data['roles']
        except KeyError:
            self.roles=None
        else:
            self.roles={guild.all_role[int(role_id)] for role_id in role_ids}
        
        try:
            user_data=data['user']
        except KeyError:
            pass
        else:
            self.user=User(user_data)

        self.available=data.get('available',True)
            
    def _update(self,data):
        guild=self.guild
        old={}
        
        require_colons=data.get('require_colons',False)
        if self.require_colons!=require_colons:
            old['require_colons']=self.require_colons
            self.require_colons=require_colons
            
        managed=data.get('managed',False)
        if self.managed!=managed:
            old['managed']=self.managed
            self.managed=managed

        animated=data.get('animated',False)
        if self.animated!=animated:
            old['animated']=self.animated
            self.animated=animated

        name=data['name']
        if name is None:
            name=''
        if self.name!=name:
            old['name']=self.name
            self.name=name
        
        try:
            role_ids=data['roles']
        except KeyError:
            roles=None
        else:
            roles={guild.all_role[int(role_id)] for role_id in role_ids}
        
        if (self.roles is None):
            if (roles is not None):
                old['roles']=None
                self.roles=roles
        else:
            if (roles is None):
                old['roles']=self.roles
                self.roles=None
            elif self.roles!=roles:
                old['roles']=self.roles
                self.roles=roles
        
        try:
            user_data=data['user']
        except KeyError:
            pass
        else:
            self.user=User(user_data)
        
        available=data.get('available',True)
        if self.available!=available:
            old['available']=self.available
            self.available=available
            
        return old
 
class reaction_mapping_line(set):
    __slots__=('unknown',)
    
    def __init__(self,unknown):
        self.unknown=unknown
    
    def __len__(self):
        return set.__len__(self)+self.unknown
    
    def __repr__(self):
        result=[self.__class__.__name__,'({']
        
        # set indexing is not public, so we need to do a check, like this
        if set.__len__(self):
            for user in self:
                result.append(repr(user))
                result.append(', ')
            
            result[-1]='}'
        else:
            result.append('}')
        
        unknown=self.unknown
        if unknown:
            result.append(', unknown=')
            result.append(repr(unknown))
        
        result.append(')')
        
        return ''.join(result)
    
    @classmethod
    def _full(cls,users):
        self=set.__new__(cls)
        set.__init__(self,users)
        self.unknown=0
        return self
    
    @staticmethod
    def _relative_id_index(self,user_id):
        bot=0
        top=len(self)
        while True:
            if bot<top:
                half=(bot+top)>>1
                if self[half].id<user_id:
                    bot=half+1
                else:
                    top=half
                continue
            break
        return bot
    
    def update(self,users):
        ln_old=len(self)
        set.update(self,users)
        ln_new=len(self)
        self.unknown-=(ln_new-ln_old)
    
    def copy(self):
        new=set.__new__(type(self))
        set.__init__(new,self)
        new.unknown=self.unknown
        return new
    
    #executes an api request if we know we know all reacters
    def filter_after(self,limit,after):
        list_form=sorted(self)
        index=self._relative_id_index(list_form,after+1) # do not include the specified id
        length=len(list_form)
        result=[]
        
        while True:
            if index==length:
                break
            
            if limit<=0:
                break
            
            result.append(list_form[index])
            index+=1
            limit-=1
            continue
        
        return result
    
    def clear(self):
        clients=[]
        for user in self:
            if type(user) is User:
                continue
            clients.append(user)

        self.unknown += (set.__len__(self) - len(clients))
        set.clear(self)
        set.update(self,clients)

class reaction_mapping(dict):
    __slots__=('fully_loaded',)
    def __init__(self,data):
        if (data is None) or (not data):
            self.fully_loaded=True
            return
        self.fully_loaded=False
        for line in data:
            self[PartialEmoji(line['emoji'])]=reaction_mapping_line(line.get('count',1))
        
    def __len__(self):
        count=0
        for line in self.values():
            count+=set.__len__(line)
            count+=line.unknown
        return count
    
    # Avoid looping over the object, just get it's source length
    def __bool__(self):
        if dict.__len__(self):
            return True
        return False
    
    def clear(self):
        for value in self.values():
            value.clear()
        if self.fully_loaded:
            self._full_check()
    
    def add(self,emoji,user):
        try:
            line=self[emoji]
        except KeyError:
            line=reaction_mapping_line(0)
            self[emoji]=line
        line.add(user)
    
    def remove(self,emoji,user):
        try:
            line=self[emoji]
        except KeyError:
            return

        if set.__len__(line):
            try:
                line.remove(user)
            except KeyError:
                pass
            else:
                if set.__len__(line) or line.unknown:
                    return
                del self[emoji]
                return
        
        if line.unknown:
            line.unknown-=1
            if set.__len__(line):
                if line.unknown:
                    return
                self._full_check()
                return
            if line.unknown:
                return
            del self[emoji]
    
    def remove_emoji(self,emoji):
        line=self.pop(emoji,None)
        if line is None:
            return
        
        if line.unknown:
            self._full_check()
        
        return line
    
    #this function is called if an emoji loses all it's unknown reacters
    def _full_check(self):
        for line in self.values():
            if line.unknown:
                self.fully_loaded=False
                return 
        
        self.fully_loaded=True
        
    #we call this when we get SOME reacters of an emoji
    def _update_some_users(self,emoji,users):
        self[emoji].update(users)
        self._full_check()
        
    def _update_all_users(self,emoji,users):
        self[emoji]=reaction_mapping_line._full(users)
        self._full_check()

BUILTIN_EMOJIS={}
UNICODE_TO_EMOJI={}

def load_builtin_emojis():
    import os, re
    from ast import literal_eval
    key=re.compile('([^:]*):(.*)$')
    with open(os.path.join(os.path.split(__spec__.origin)[0],'emojis.dnd'),mode='r') as file:
        emoji_id=1
        for line in file.readlines():

            parsed=key.match(line)
            if parsed is None:
                if line=='\n' or line=='':
                    continue
                raise RuntimeError(f'When loading builtin emojis:\n`{line}`\nCould not be parsed.')
            
            name,value=parsed.groups()
            value=literal_eval(value).decode('utf8')
            
            emoji=object.__new__(Emoji)
            emoji.animated      = False
            emoji.id            = emoji_id
            emoji.name          = name
            emoji.unicode       = value
            emoji.guild         = None
            emoji.roles         = None
            emoji.managed       = False
            emoji.require_colons= True
            emoji.user          = ZEROUSER
            emoji.available     = True
            EMOJIS[emoji_id]    = emoji
            
            UNICODE_TO_EMOJI[value]=emoji
            BUILTIN_EMOJIS[name]=emoji
            
            emoji_id=emoji_id+1
            
            
load_builtin_emojis()

def parse_emoji(text):
    custom=EMOJI_RP.fullmatch(text)
    if custom is None:
        try:
            emoji=UNICODE_TO_EMOJI[text]
        except KeyError:
            return
        else:
            if text==emoji.unicode:
                return emoji

    args=custom.groups()
    emoji_id            = int(args[3])
    try:
        emoji           = EMOJIS[emoji_id]
        if emoji.guild is None:
            emoji.name  = args[1]
    except KeyError:
        emoji           = object.__new__(Emoji)
        emoji.id        = emoji_id
        emoji.animated  = bool(args[0])
        emoji.name      = args[1]
        emoji.unicode   = None
        emoji.guild     = None
        emoji.available = True
        
    return emoji

activity.PartialEmoji=PartialEmoji

del activity
del URLS
