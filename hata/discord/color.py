# -*- coding: utf-8 -*-
__all__ = ('Color', 'DefaultAvatar', )

from .http import URLS

class Color(int):
    __slots__=()

    def __repr__(self):
        return f'<{self.__class__.__name__} #{self:06X}>'

    @property
    def as_html(self):
        return f'#{self:06X}'

    @classmethod
    def from_html(cls,value):
        if len(value)!=7:
            raise ValueError
        return cls(value[1:],base=16)

    @classmethod
    def from_tuple(cls,value):
        return cls((value[0]<<16)|(value[1]<<8)|value[2])

    @property
    def as_tuple(self):
        return (self>>16,(self>>8)&0x00ff,self&0x0000ff)

    @classmethod
    def from_rgb(cls,r,g,b):
        return cls((r<<16)|(g<<8)|b)

    @property
    def red(self):
        return self>>16

    @property
    def green(self):
        return (self>>8)&0x0000ff

    @property
    def blue(self):
        return self&0x0000ff


class DefaultAvatar(object):
    # class related
    INSTANCES = [NotImplemented] * 5
    COUNT = 5
    
    @classmethod
    def for_(cls,user):
        return cls.INSTANCES[user.discriminator%cls.COUNT]
    
    # object related
    __slots__=('color', 'name', 'value',)
    
    def __init__(self,value,name,color):
        self.value=value
        self.name=name
        self.color=color
        self.INSTANCES[value]=self
        
    def __str__(self):
        return self.name

    def __int__(self):
        return self.value

    def __repr__(self):
        return f'<{self.__class__.__name__} name={self.name} value={self.value}>'

    url=property(URLS.default_avatar_url)
    
    # predefined
    blue    = NotImplemented
    gray    = NotImplemented
    green   = NotImplemented
    orange  = NotImplemented
    red     = NotImplemented

DefaultAvatar.blue      = DefaultAvatar(0,  'blue',     Color(0x7289da))
DefaultAvatar.gray      = DefaultAvatar(1,  'gray',     Color(0x747f8d))
DefaultAvatar.green     = DefaultAvatar(2,  'green',    Color(0x43b581))
DefaultAvatar.orange    = DefaultAvatar(3,  'orange',   Color(0xfaa61a))
DefaultAvatar.red       = DefaultAvatar(4,  'red',      Color(0xf04747))

#parse color formats
def _parse_c_fs(value):
    if type(value) is Color:
        return value
    if type(value) is int:
        if value:
            return Color(value)
        return Color(0)
    raise TypeError(f'Color can be `Color` or `int` type, got {value.__class__.__name__}')
    
del URLS
