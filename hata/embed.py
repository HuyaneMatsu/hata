# -*- coding: utf-8 -*-
__all__ = ('EXTRA_EMBED_TYPES', 'Embed', 'EmbedAuthor', 'EmbedCore',
    'EmbedField', 'EmbedFooter', 'EmbedImage', 'EmbedProvider',
    'EmbedThumbnail', 'EmbedVideo', )

import re

from .others import ROLE_MENTION_RP, USER_MENTION_RP, CHANNEL_MENTION_RP,   \
    parse_time, urlcutter
from .color import Color

EXTRA_EMBED_TYPES=('application_news', 'article', 'gifv', 'image', 'link', 'video')

def _convert_content(content,message):
    escape=re.escape
    transformations = {
        '@everyone':'@\u200beveryone',
        '@here':'@\u200bhere'
            }
    
    guild=message.channel.guild

    if guild is None:
        users=message.channel.users
        for id_ in USER_MENTION_RP.findall(content):
            id_=int(id_)
            for user in users:
                if user.id==id_:
                    transformations[escape(f'<@{id_}>')]=f'@{user.name}'
                    break
    else:
        channels=guild.all_channel
        for id_ in CHANNEL_MENTION_RP.findall(content):
            id_=int(id_)
            try:
                channel=channels[id_]
            except KeyError:
                continue
            transformations[escape(f'<#{id_}>')]=f'#{channel.name}'
        
        users=guild.users
        for id_ in USER_MENTION_RP.findall(content):
            id_=int(id_)
            try:
                user=users[id_]
            except KeyError:
                continue
            profile=user.guild_profiles.get(guild,None)
            if profile is None or profile.nick is None:
                name=f'@{user.name}'
            else:
                name=f'@{profile.nick}'
                
            transformations[escape(f'<@!{id_}>')]=name
            transformations[escape(f'<@{id_}>')]=name

        roles=guild.all_role
        for id_ in ROLE_MENTION_RP.findall(content):
            id_=int(id_)
            try:
                role=roles[id_]
            except KeyError:
                continue
            transformations[escape(f'<@&{id_}>')]=f'@{role.name}'
        
        return re.compile("|".join(transformations)).sub(lambda mention:transformations[escape(mention.group(0))],content)

class EmbedThumbnail(object):
    __slots__=('height', 'proxy_url', 'url', 'width',)
    def __init__(self,url):
        self.url            = url
        self.proxy_url      = None
        self.height         = 0
        self.width          = 0
        
    @classmethod
    def from_data(cls,data):
        self=object.__new__(cls)
        self.url            = data.get('url',None)
        self.proxy_url      = data.get('proxy_url',None)
        self.height         = data.get('height',0)
        self.width          = data.get('width',0)
        
        return self
    
    def to_data(self):
        return {
            'url'           : self.url,
                }
    
    def __len__(self):
        return 0
    
    def __repr__(self):
        text = [
            '<',
            self.__class__.__name__,
            ' url=',
                ]
        
        url=self.url
        if url is None:
            text.append('None')
        else:
            text.append('\'')
            url=urlcutter(url)
            text.append(url)
            text.append('\'')
        
        text.append(', size=')
        text.append(str(self.width))
        text.append('x')
        text.append(str(self.height))
    
        text.append('>')
        
        return ''.join(text)
    
    def __eq__(self,other):
        if self.url is None:
            if other.url is not None:
                return False
        else:
            if other.url is None:
                return False
            if self.url!=other.url:
                return False
        
        return True
    
class EmbedVideo(object):
    __slots__=('height', 'url', 'width',)

    def __init__(self):
        self.url            = None
        self.height         = 0
        self.width          = 0

    @classmethod
    def from_data(cls,data):
        self=object.__new__(cls)
        self.url            = data.get('url',None)
        self.height         = data.get('height',0)
        self.width          = data.get('width',0)
        
        return self
    
    def to_data(self):
        return {}
    
    def __len__(self):
        return 0
    
    def __repr__(self):
        text = [
            '<',
            self.__class__.__name__,
            ' url=',
                ]
        
        url=self.url
        if url is None:
            text.append('None')
        else:
            text.append('\'')
            url=urlcutter(url)
            text.append(url)
            text.append('\'')
        
        text.append(', size=')
        text.append(str(self.width))
        text.append('x')
        text.append(str(self.height))
    
        text.append('>')
        
        return ''.join(text)
    
    def __eq__(self,other):
        if self.url is None:
            if other.url is not None:
                return False
        else:
            if other.url is None:
                return False
            if self.url!=other.url:
                return False
        
        return True
    
class EmbedImage(object):
    __slots__=('height', 'proxy_url', 'url', 'width',)
    def __init__(self,url):
        self.url            = url
        self.proxy_url      = None
        self.height         = 0
        self.width          = 0
        
    @classmethod
    def from_data(cls,data):
        self=object.__new__(cls)
        self.url            = data.get('url',None)
        self.proxy_url      = data.get('proxy_url',None)
        self.height         = data.get('height',0)
        self.width          = data.get('width',0)
        
        return self
    
    def to_data(self):
        return {
            'url'           : self.url,
                }
    
    def __len__(self):
        return 0
    
    def __repr__(self):
        text = [
            '<',
            self.__class__.__name__,
            ' url=',
                ]
        
        url=self.url
        if url is None:
            text.append('None')
        else:
            text.append('\'')
            url=urlcutter(url)
            text.append(url)
            text.append('\'')
            
        text.append(', size=')
        text.append(str(self.width))
        text.append('x')
        text.append(str(self.height))
        
        text.append('>')
        
        return ''.join(text)
    
    def __eq__(self,other):
        if self.url is None:
            if other.url is not None:
                return False
        else:
            if other.url is None:
                return False
            if self.url!=other.url:
                return False
        
        return True
    
class EmbedProvider(object):
    __slots__=('name', 'url',)
    
    def __init__(self):
        self.name           = None
        self.url            = None
        
    @classmethod
    def from_data(cls,data):
        self=object.__new__(cls)
        self.name           = data.get('name',None)
        self.url            = data.get('url',None)
        
        return self
    
    def __len__(self):
        name=self.name
        if name is None:
            return 0
        return len(name)
        
    def __repr__(self):
        text = [
            '<',
            self.__class__.__name__,
            ' length=',
            str(self.__len__()),
            ', url='
                ]
        
        url=self.url
        if url is None:
            text.append('None')
        else:
            text.append('\'')
            url=urlcutter(url)
            text.append(url)
            text.append('\'')
        
        text.append('>')
        
        return ''.join(text)
    
    def to_data(self):
        return {}
        
    def __eq__(self,other):
        if self.name is None:
            if other.name is not None:
                return False
        else:
            if other.name is None:
                return False
            if self.name!=other.name:
                return False
            
        if self.url is None:
            if other.url is not None:
                return False
        else:
            if other.url is None:
                return False
            if self.name!=other.name:
                return False
        
        return True
    
class EmbedAuthor(object):
    __slots__=('icon_url', 'name', 'proxy_icon_url', 'url',)
    def __init__(self,icon_url=None,name=None,url=None):
        self.icon_url       = icon_url
        self.name           = name
        self.url            = url
        self.proxy_icon_url = None
    
    @classmethod
    def from_data(cls,data):
        self=object.__new__(cls)
        self.name           = data.get('name',None)
        self.url            = data.get('url',None)
        self.icon_url       = data.get('icon_url',None)
        self.proxy_icon_url = data.get('proxy_icon_url',None)
        
        return self
    
    def to_data(self):
        result={}
    
        name=self.name
        if name is not None:
            result['name']  = name
        
        url=self.url
        if url is not None:
            result['url']   = url
        
        icon_url=self.icon_url
        if icon_url is not None:
            result['icon_url']=icon_url
            
        return result

    def __len__(self):
        name=self.name
        if name is None:
            return 0
        return len(self.name)
    
    def __repr__(self):
        text = [
            '<',
            self.__class__.__name__,
            ' length=',
            str(self.__len__()),
            ', url='
                ]
        
        url=self.url
        if url is None:
            text.append('None')
        else:
            text.append('\'')
            url=urlcutter(url)
            text.append(url)
            text.append('\'')
        
        text.append(', icon_url=')
        icon_url=self.icon_url
        if icon_url is None:
            text.append('None')
        else:
            text.append('\'')
            icon_url=urlcutter(icon_url)
            text.append(icon_url)
            text.append('\'')
            
        text.append('>')
        
        return ''.join(text)
    
    def __eq__(self,other):
        if self.icon_url is None:
            if other.icon_url is not None:
                return False
        else:
            if other.icon_url is None:
                return False
            if self.icon_url!=other.icon_url:
                return False
        
        if self.name is None:
            if other.name is not None:
                return False
        else:
            if other.name is None:
                return False
            if self.name!=other.name:
                return False
        
        if self.url is None:
            if other.url is not None:
                return False
        else:
            if other.url is None:
                return False
            if self.url!=other.url:
                return False
        
        return True
    
class EmbedFooter(object):
    __slots__=('icon_url', 'proxy_icon_url', 'text',)
    def __init__(self,text,icon_url=None):
        self.text           = text
        self.icon_url       = icon_url
        self.proxy_icon_url = None
        
    @classmethod
    def from_data(cls,data):
        self=object.__new__(cls)
        self.text           = data['text']
        self.icon_url       = data.get('icon_url',None)
        self.proxy_icon_url = data.get('proxy_icon_url',None)
        
        return self
    
    def to_data(self):
        result = {
            'text'          : self.text,
                }
        
        icon_url=self.icon_url
        if icon_url is not None:
            result['icon_url']= icon_url
            
        return result
    
    def __len__(self):
        return len(self.text)
    
    def __repr__(self):
        text = [
            '<',
            self.__class__.__name__,
            ' length=',
            str(self.__len__()),
            ', url='
                ]
        
        icon_url=self.icon_url
        if icon_url is None:
            text.append('None')
        else:
            text.append('\'')
            icon_url=urlcutter(icon_url)
            text.append(icon_url)
            text.append('\'')
        
        text.append('>')
        
        return ''.join(text)
        
    def __eq__(self,other):
        if self.icon_url is None:
            if other.icon_url is not None:
                return False
        else:
            if other.icon_url is None:
                return False
            if self.icon_url!=other.icon_url:
                return False
        
        if self.text!=other.text:
            return False
        
        return True
    
class EmbedField(object):
    __slots__=('inline', 'name', 'value',)
    def __init__(self,name,value,inline=False):
        self.name           = name
        self.value          = value
        self.inline         = inline
        
    @classmethod
    def from_data(cls,data):
        self=object.__new__(cls)
        
        self.name           = data['name']
        self.value          = data['value']
        self.inline         = data.get('inline',False)
        
        return self

    def to_data(self):
        result = {
            'name'          : self.name,
            'value'         : self.value,
                }
        
        inline=self.inline
        if inline:
            result['inline']= inline

        return result
    
    def __len__(self):
        return len(self.name)+len(self.value)
    
    def __repr__(self):
        return f'<{self.__class__.__name__} length={self.__len__()}, inline={self.inline}>'

    def __eq__(self,other):
        if self.name!=other.name:
            return False
        
        if self.value!=other.value:
            return False
        
        if self.inline!=other.inline:
            return False
        
        return True
        
class EmbedCore(object):
    __slots__=('author', 'color', 'description', 'fields', 'footer', 'image',
        'provider', 'thumbnail', 'timestamp', 'title', 'type', 'url', 'video',)

    def __init__(self,title=None,description=None,color=None,url=None,timestamp=None,type_='rich'):
        self.title          = title
        self.description    = description
        self.color          = color
        self.url            = url
        self.timestamp      = timestamp
        self.type           = type_ #must be `rich` for webhook embeds
        self.footer         = None
        self.image          = None
        self.thumbnail      = None
        self.video          = None
        self.provider       = None
        self.author         = None
        self.fields         = []
    
    @classmethod
    def from_data(cls,data):
        self=cls.__new__(cls)
        
        self.title          = data.get('title',None)
        self.type           = data.get('type',None)
        self.description    = data.get('description',None)
        self.url            = data.get('url',None)

        try:
            timestamp_data = data['timestamp']
        except KeyError:
            self.timestamp  = None
        else:
            self.timestamp  = parse_time(timestamp_data)
        
        try:
            color_data      = data['color']
        except KeyError:
            self.color      = None
        else:
            self.color      = Color(color_data)

        try:
            footer_data     = data['footer']
        except KeyError:
            self.footer     = None
        else:
            self.footer     = EmbedFooter.from_data(footer_data)
        
        try:
            image_data      = data['image']
        except KeyError:
            self.image      = None
        else:
            self.image      = EmbedImage.from_data(image_data)
        
        try:
            thumbnail_data  = data['thumbnail']
        except KeyError:
            self.thumbnail  = None
        else:
            self.thumbnail  = EmbedThumbnail.from_data(thumbnail_data)

        try:
            video_data      = data['video']
        except KeyError:
            self.video      = None
        else:
            self.video      = EmbedVideo.from_data(video_data)
        
        try:
            provider_data   = data['provider']
        except KeyError:
            self.provider   = None
        else:
            self.provider   = EmbedProvider.from_data(provider_data)
        
        try:
            author_data     = data['author']
        except KeyError:
            self.author     = None
        else:
            self.author     = EmbedAuthor.from_data(author_data)
            
        try:
            field_datas     = data['fields']
        except KeyError:
            self.fields     = []
        else:
            self.fields     = [EmbedField.from_data(field_data) for field_data in field_datas]
        
        return self

    def to_data(self):
        data = {}
        
        type=self.type
        if type is not None:
            data['type']        = type
        
        title=self.title
        if title is not None:
            data['title']       = title
        
        description=self.description
        if description is not None:
            data['description'] = description
            
        color=self.color
        if color is not None:
            data['color']       = color
        
        url=self.url
        if url is not None:
            data['url']         = url
        
        timestamp=self.timestamp
        if timestamp is not None:
            data['timestamp']   = timestamp.isoformat()

        footer=self.footer
        if footer is not None:
            data['footer']      = footer.to_data()
        
        image=self.image
        if image is not None:
            data['image']       = image.to_data()
        
        thumbnail=self.thumbnail
        if thumbnail is not None:
            data['thumbnail']   = thumbnail.to_data()
        
        author=self.author
        if author is not None:
            data['author']      = author.to_data()
        
        if self.fields:
            data['fields']      = [field.to_data() for field in self.fields]
        
        return data

    def _update_sizes(self,data):
        changed=0
        try:
            image_data=data['image']
        except KeyError:
            pass
        else:
            image=self.image
            if image is None:
                self.image      = EmbedImage.from_data(image_data)
            else:
                image.height    = image_data.get('height',0)
                image.width     = image_data.get('width',0)
            changed=1
        
        try:
            thumbnail_data=data['thumbnail']
        except KeyError:
            pass
        else:
            thumbnail=self.thumbnail
            if thumbnail is None:
                self.thumbnail  = EmbedThumbnail.from_data(thumbnail_data)
            else:
                thumbnail.height= thumbnail_data.get('height',0)
                thumbnail.width = thumbnail_data.get('width',0)
            changed=1

        try:
            video_data=data['video']
        except KeyError:
            pass
        else:
            video=self.video
            if video is None:
                self.video      = EmbedVideo.from_data(video_data)
            else:
                video.height    = video_data.get('height',0)
                video.width     = video_data.get('width',0)
            changed=1

        return changed

    def _update_sizes_no_return(self,data):
        try:
            image_data=data['image']
        except KeyError:
            pass
        else:
            image=self.image
            if image is None:
                self.image      = EmbedImage.from_data(image_data)
            else:
                image.height    = image_data.get('height',0)
                image.width     = image_data.get('width',0)

        try:
            thumbnail_data=data['thumbnail']
        except KeyError:
            pass
        else:
            thumbnail=self.thumbnail
            if thumbnail is None:
                self.thumbnail  = EmbedThumbnail.from_data(thumbnail_data)
            else:
                thumbnail.height= thumbnail_data.get('height',0)
                thumbnail.width = thumbnail_data.get('width',0)

        try:
            video_data=data['video']
        except KeyError:
            pass
        else:
            video=self.video
            if video is None:
                self.video      = EmbedVideo.from_data(video_data)
            else:
                video.height    = video_data.get('height',0)
                video.width     = video_data.get('width',0)

    def __len__(self):
        result=0
        
        title=self.title
        if title is not None:
            result+=len(title)
            
        description=self.description
        if description is not None:
            result+=len(description)
        
        title=self.title
        if title is not None:
            result+=len(title)
        
        footer=self.footer
        if footer is not None:
            result+=len(footer.text)
        
        author=self.author
        if author is not None:
            name=author.name
            if name is not None:
                result+=len(name)
        
        for field in self.fields:
            result+=len(field.name)
            result+=len(field.value)

        return result
    
    def __repr__(self):
        return f'<{self.__class__.__name__} length={self.__len__()}>'
    
    def __eq__(self,other):
        if type(self) is not type(other):
            try:
                other=other.source
            except AttributeError:
                return NotImplemented
            if type(self) is not type(other):
                return NotImplemented
        
        if self.title is None:
            if other.title is not None:
                return False
        else:
            if other.title is None:
                return False
            if self.title!=other.title:
                return False
            
        if self.description is None:
            if other.description is not None:
                return False
        else:
            if other.description is None:
                return False
            if self.description!=other.description:
                return False
        
        if self.color is None:
            if other.color is not None:
                return False
        else:
            if other.color is None:
                return False
            if self.color!=other.color:
                return False
        
        if self.url is None:
            if other.url is not None:
                return False
        else:
            if other.url is None:
                return False
            if self.url!=other.url:
                return False
            
        if self.timestamp is None:
            if other.timestamp is not None:
                return False
        else:
            if other.timestamp is None:
                return False
            if self.timestamp!=other.timestamp:
                return False
            
        if self.type is None:
            if other.type is not None:
                return False
        else:
            if other.type is None:
                return False
            if self.type!=other.type:
                return False
        
        if self.footer is None:
            if other.footer is not None:
                return False
        else:
            if other.footer is None:
                return False
            if self.footer!=other.footer:
                return False
            
        if self.image is None:
            if other.image is not None:
                return False
        else:
            if other.image is None:
                return False
            if self.image!=other.image:
                return False
            
        if self.thumbnail is None:
            if other.thumbnail is not None:
                return False
        else:
            if other.thumbnail is None:
                return False
            if self.thumbnail!=other.thumbnail:
                return False
        
        if self.video is None:
            if other.video is not None:
                return False
        else:
            if other.video is None:
                return False
            if self.video!=other.video:
                return False
        
        if self.author is None:
            if other.author is not None:
                return False
        else:
            if other.author is None:
                return False
            if self.author!=other.author:
                return False
        
        if self.fields!=other.fields:
            return False
        
        return True
        

    @property
    def contents(self):
        result=[]
        
        title=self.title
        if title is not None:
            result.append(title)
            
        description=self.description
        if description is not None:
            result.append(description)
            
        author=self.author
        if author is not None:
            name=author.name
            if name is not None:
                result.append(name)

        footer=self.footer
        if footer is not None:
            result.append(footer.text)

        for field in self.fields:
            result.append(field.name)
            result.append(field.value)

        return result

    def _clean_copy(self,message):
        new=object.__new__(type(self))
        
        new.title           = self.title
        new.description     = None if self.description is None else _convert_content(self.description,message)
        new.color           = self.color
        new.url             = self.url
        new.timestamp       = self.timestamp
        new.type            = self.type
        
        new.footer          = self.footer
        new.image           = self.image
        new.thumbnail       = self.thumbnail
        new.video           = self.video
        new.provider        = self.provider
        new.author          = self.author
        new.fields          = [type(field)(field.name,_convert_content(field.value,message),inline=field.inline) for field in self.fields]

        return new
        
class Embed(object):
    __slots__=('data',)
    def __init__(self,title=None,description=None,color=None,url=None,timestamp=None,type_='rich'):
        self.data = data = {}
        
        if (title is not None):
            data['title']       = title
            
        if (description is not None):
            data['description'] = description
            
        if (color is not None):
            data['color']       = color
            
        if (url is not None):
            data['url']         = url
            
        if (timestamp is not None):
            data['timestamp']   = timestamp.isoformat()
            
        if (type_ is not None):
            data['type']        = type_

    def to_data(self):
        return self.data
    
    #author
    def _get_author(self):
        try:
            data=self.data['author']
        except KeyError:
            return
        return EmbedAuthor.from_data(data)
    
    def _set_author(self,value):
        self.data['author']=value.to_data()
    def _del_author(self):
        try:
            del self.data['author']
        except KeyError:
            pass
    author=property(_get_author, _set_author, _del_author)
    del _get_author, _set_author, _del_author
    
    def add_author(self,icon_url=None,name=None,url=None):
        data = {}

        if (name is not None):
            data['name']    = name
        
        if (url is not None):
            data['url']     = url
        
        if (icon_url is not None):
            data['icon_url']= icon_url
        
        self.data['author']=data
        return self

    #color
    def _get_color(self):
        return self.data.get('color',None)
    def _set_color(self,value):
        self.data['color']=value
    def _del_color(self,value):
        try:
            del self.data['color']
        except KeyError:
            pass
    color=property(_get_color, _set_color, _del_color)
    del _get_color, _set_color, _del_color

    #description
    def _get_description(self):
        return self.data.get('description',None)
    def _set_description(self,value):
        self.data['description']=value
    def _del_description(self):
        try:
            del self.data['description']
        except KeyError:
            pass
    description=property(_get_description, _set_description, _del_description)
    del _get_description, _set_description, _del_description

    #fields
    def _get_fields(self):
        try:
            field_datas=self.data['fields']
        except KeyError:
            self.data['fields']=field_datas=[]
        return _EmbedFieldsReflection(field_datas)
    def _set_fields(self,value):
        if type(value) is _EmbedFieldsReflection:
            self.data['fields']=value.data
        else:
            self.data=[field.to_data() if type(field) is EmbedField else field for field in value]
    def _del_fields(self):
        try:
            field_datas=self.data.pop('fields')
        except KeyError:
            pass
        else:
            field_datas.clear()
    fields=property(_get_fields, _set_fields, _del_fields)
    del _get_fields, _set_fields, _del_fields
    
    def add_field(self,name,value,inline=False):
        data = {
            'name'  : name,
            'value' : value,
                }
        
        if inline:
            data['inline']  = inline

        try:
            fields=self.data['fields']
        except KeyError:
            self.data['fields']=[data]
        else:
            fields.append(data)
        return self

    def insert_field(self,index,name,value,inline=False):
        data = {
            'name'  : name,
            'value' : value,
                }
        
        if inline:
            data['inline']  = inline

        try:
            fields=self.data['fields']
        except KeyError:
            self.data['fields']=[data]
        else:
            fields.insert(index,data)

    def get_field(self,index):
        try:
            fields=self.data['fields']
        except KeyError:
            raise IndexError(index) from None
        field_data=fields[index]
        return EmbedField.from_data(field_data)

    def set_field(self,index,field):
        try:
            fields=self.data['fields']
        except KeyError:
            raise IndexError(index) from None
        field_data=field.to_data()
        fields[index]=field_data

    def del_field(self,index):
        try:
            fields=self.data['fields']
        except KeyError:
            raise IndexError(index) from None
        del fields[index]

    #footer
    def _get_footer(self):
        try:
            data=self.data['footer']
        except KeyError:
            return
        return EmbedFooter.from_data(data)
    def _set_footer(self,value):
        self.data['footer']=value.to_data()
    def _del_footer(self):
        try:
            del self.data['footer']
        except KeyError:
            pass
    footer=property(_get_footer, _set_footer, _del_footer)
    del _get_footer, _set_footer, _del_footer
    
    def add_footer(self,text,icon_url=None):
        data = {
            'text'  : text,
                }
        
        if icon_url is not None:
            data['icon_url']= icon_url
        
        self.data['footer']=data
        return self

    #image
    def _get_image(self):
        try:
            data=self.data['image']
        except KeyError:
            return
        return EmbedImage.from_data(data)
    def _set_image(self,value):
        self.data['image']=value.to_data()
    def _del_image(self):
        try:
            del self. data['image']
        except KeyError:
            pass
    
    image=property(_get_image, _set_image, _del_image)
    del _get_image, _set_image, _del_image
    
    def add_image(self,url):
        data = {
            'url'   : url,
                }
        self.data['image']  = data
        return self

    #provider
    def _get_provider(self):
        try:
            data=self.data['provider']
        except KeyError:
            return
        return EmbedProvider.from_data(data)
    def _del_provider(self):
        try:
            del self.data['provider']
        except KeyError:
            pass
    provider=property(_get_provider, None, _del_provider)
    del _get_provider, _del_provider


    #thumbnail
    def _get_thumbnail(self):
        try:
            data=self.data['thumbnail']
        except KeyError:
            return
        return EmbedThumbnail.from_data(data)
    def _set_thumbnail(self,value):
        self.data['thumbnail']=value.to_data()
    def _del_thumbnail(self):
        try:
            self.data['thumbnail']
        except KeyError:
            pass
    thumbnail=property(_get_thumbnail, _set_thumbnail, _del_thumbnail)
    del _get_thumbnail, _set_thumbnail, _del_thumbnail
    
    def add_thumbnail(self,url):
        data = {
            'url'   : url,
                }

        self.data['thumbnail']= data
        return self

    #timestamp
    def _get_timestamp(self):
        try:
            value=self.data['timestamp']
        except KeyError:
            return
        return parse_time(value)
    def _set_timestamp(self,value):
        self.data['timestamp']=value.isoformat()
    def _del_timestamp(self):
        try:
            del self.data['timestamp']
        except KeyError:
            pass
    timestamp=property(_get_timestamp, _set_timestamp, _del_timestamp)
    del _get_timestamp, _set_timestamp, _del_timestamp

    #title
    def _get_title(self):
        return self.data.get('title',None)
    def _set_title(self,value):
        self.data['title']=value
    def _del_title(self):
        try:
            del self.data['title']
        except KeyError:
            pass
    title=property(_get_title, _set_title, _del_title)
    del _get_title, _set_title, _del_title

    #type
    def _get_type(self):
        return self.data.get('type',None)
    def _set_type(self,value):
        self.data['type']=value
    def _del_type(self,value):
        try:
            del self.data['type']
        except KeyError:
            pass
    type=property(_get_type, _set_type, _del_type)
    del _get_type, _set_type, _del_type

    #url
    def _get_url(self):
        return self.data.get('url',None)
    def _set_url(self,value):
        self.data['url']=value
    def _del_url(self):
        try:
            del self.data['url']
        except KeyError:
            pass
    url=property(_get_url, _set_url, _del_url)
    del _get_url, _set_url, _del_url

    #video
    def _get_video(self):
        try:
            data=self.data['video']
        except KeyError:
            return
        return EmbedVideo.from_data(data)
    def _del_video(self):
        try:
            del self.data['video']
        except KeyError:
            pass
    video=property(_get_video, None, _del_video)
    del _get_video, _del_video

    #rest
    def _get_source(self):
        return EmbedCore.from_data(self.data)
    def _set_source(self,value):
        self.data=value.to_data()
    def _del_source(self,value):
        self.data={}
    source=property(_get_source, _set_source, _del_source)
    del _get_source, _set_source, _del_source
    
    def __len__(self):
        data=self.data
        result=0
        
        try:
            title=data['title']
        except KeyError:
            pass
        else:
            result+=len(title)
        
        try:
            description=data['description']
        except KeyError:
            pass
        else:
            result+=len(description)
        
        try:
            author=data['author']
        except KeyError:
            pass
        else:
            try:
                name=data['name']
            except KeyError:
                pass
            else:
                result+=len(name)

        try:
            footer=data['footer']
        except KeyError:
            pass
        else:
            result+=len(footer['text'])
        
        try:
            field_datas=data['fields']
        except KeyError:
            pass
        else:
            for field_data in field_datas:
                result+=len(field_data['name'])
                result+=len(field_data['value'])

        return result
    
    def __repr__(self):
        return f'<{self.__class__.__name__} length={self.__len__()}>'
    
    def __eq__(self,other):
        return self.source==other
    
    @property
    def contents(self):
        data=self.data
        result=[]
        
        try:
            title=data['title']
        except KeyError:
            pass
        else:
            result.append(title)
            
        try:
            description=data['description']
        except KeyError:
            pass
        else:
            result.append(description)
        
        try:
            author=data['author']
        except KeyError:
            pass
        else:
            try:
                name=author['name']
            except KeyError:
                pass
            else:
                result.append(name)
        
        try:
            footer=data['footer']
        except KeyError:
            pass
        else:
            result.append(footer['text'])
        
        try:
            field_datas=data['fields']
        except KeyError:
            pass
        else:
            for field_data in field_datas:
                result.append(field_data['name'])
                result.append(field_data['value'])

        return result

class _EmbedFieldsReflection(object):
    __slots__=('data',)
    def __init__(self,data):
        self.data=data
        
    def clear(self):
        self.data.clear()

    def __len__(self):
        return self.data.__len__()
    
    def __repr__(self):
        return f'<{self.__class__.__name__} fields={self.data.__len__()}>'
    
    def __getitem__(self,index):
        return EmbedField.from_data(self.data[index])
    
    def __setitem__(self,index,field):
        self.data[index]=field.to_data()

    def __delitem__(self,index):
        del self.data[index]

    def append(self,field):
        self.data.append(field.to_data())

    def insert(self,index,field):
        self.data.insert(index,field.to_data())

    def add_field(self,name,value,inline=False):
        data = {
            'name'  : name,
            'value' : value,
                }
        
        if inline:
            data['inline']  = inline

        self.data.append(data)

    def insert_field(self,index,name,value,inline=False):
        data = {
            'name'  : name,
            'value' : value,
                }
        
        if inline:
            data['inline']  = inline

        self.data.insert(index,data)
            
    def __iter__(self):
        for field_data in self.data:
            yield EmbedField.from_data(field_data)

    def __reversed__(self):
        for field_data in reversed(self.data):
            yield EmbedField.from_data(field_data)
