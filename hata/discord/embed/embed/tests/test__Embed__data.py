from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....color import Color
from ....utils import datetime_to_timestamp

from ...embed_author import EmbedAuthor
from ...embed_field import EmbedField
from ...embed_footer import EmbedFooter
from ...embed_image import EmbedImage
from ...embed_provider import EmbedProvider
from ...embed_thumbnail import EmbedThumbnail
from ...embed_video import EmbedVideo

from ..embed import Embed
from ..preinstanced import EmbedType

from .test__Embed__constructor import _assert_fields_set


def test__Embed__from_data():
    """
    Tests whether ``Embed.from_data`` works as intended.
    """
    author = EmbedAuthor('author name')
    color = Color(123)
    description = 'embed description'
    embed_type = EmbedType.video
    fields = [EmbedField('komeiji', 'koishi'), EmbedField('komeiji', 'satori', inline = True)]
    footer = EmbedFooter('footer text')
    image = EmbedImage('attachment://image')
    provider = EmbedProvider('provider name')
    thumbnail = EmbedThumbnail('attachment://thumbnail')
    timestamp = DateTime(2016, 5, 5, tzinfo = TimeZone.utc)
    title = 'embed title'
    url = 'https://orindance.party/'
    video = EmbedVideo('attachment://video')
    
    data = {
        'author': author.to_data(defaults = True, include_internals = True),
        'color': int(color),
        'description': description,
        'type': embed_type.value,
        'fields': [field.to_data(defaults = True, include_internals = True) for field in fields],
        'footer': footer.to_data(defaults = True, include_internals = True),
        'image': image.to_data(defaults = True, include_internals = True),
        'provider': provider.to_data(defaults = True, include_internals = True),
        'thumbnail': thumbnail.to_data(defaults = True, include_internals = True),
        'timestamp': datetime_to_timestamp(timestamp),
        'title': title,
        'url': url,
        'video': video.to_data(defaults = True, include_internals = True),
    }
    
    embed = Embed.from_data(data)
    _assert_fields_set(embed)
    
    vampytest.assert_eq(embed.author, author)
    vampytest.assert_eq(embed.color, color)
    vampytest.assert_eq(embed.description, description)
    vampytest.assert_eq(embed.fields, fields)
    vampytest.assert_eq(embed.footer, footer)
    vampytest.assert_eq(embed.image, image)
    vampytest.assert_eq(embed.provider, provider)
    vampytest.assert_eq(embed.thumbnail, thumbnail)
    vampytest.assert_eq(embed.timestamp, timestamp)
    vampytest.assert_eq(embed.title, title)
    vampytest.assert_eq(embed.type, embed_type)
    vampytest.assert_eq(embed.url, url)
    vampytest.assert_eq(embed.video, video)


def test__Embed__to_data():
    """
    Tests whether ``Embed.to_data`` works as intended.
    
    Case: Include defaults and internals.
    """
    author = EmbedAuthor('author name')
    color = Color(123)
    description = 'embed description'
    embed_type = EmbedType.video
    fields = [EmbedField('komeiji', 'koishi'), EmbedField('komeiji', 'satori', inline = True)]
    footer = EmbedFooter('footer text')
    image = EmbedImage('attachment://image')
    provider = EmbedProvider('provider name')
    thumbnail = EmbedThumbnail('attachment://thumbnail')
    timestamp = DateTime(2016, 5, 5, tzinfo = TimeZone.utc)
    title = 'embed title'
    url = 'https://orindance.party/'
    video = EmbedVideo('attachment://video')
    
    embed = Embed(
        author = author,
        color = color,
        description = description,
        embed_type = embed_type,
        fields = fields,
        footer = footer,
        image = image,
        provider = provider,
        thumbnail = thumbnail,
        timestamp = timestamp,
        title = title,
        url = url,
        video = video
    )
    
    expected_output = {
        'author': author.to_data(defaults = True, include_internals = True),
        'color': int(color),
        'description': description,
        'type': embed_type.value,
        'fields': [field.to_data(defaults = True, include_internals = True) for field in fields],
        'footer': footer.to_data(defaults = True, include_internals = True),
        'image': image.to_data(defaults = True, include_internals = True),
        'provider': provider.to_data(defaults = True, include_internals = True),
        'thumbnail': thumbnail.to_data(defaults = True, include_internals = True),
        'timestamp': datetime_to_timestamp(timestamp),
        'title': title,
        'url': url,
        'video': video.to_data(defaults = True, include_internals = True),
    }
    
    vampytest.assert_eq(
        embed.to_data(defaults = True, include_internals = True),
        expected_output,
    )



def test__Embed__update_sizes__no_change():
    """
    Tests whether ``Embed._update_sizes`` works as intended.
    
    Case: No changes.
    """
    embed = Embed()
    output = embed._update_sizes({})
    
    vampytest.assert_eq(output, 0)


def test__Embed__update_sises__all_change():
    """
    Tests whether ``Embed._update_sizes`` works as intended.
    
    Case: All changed.
    """
    image_height = 1000
    image_proxy_url = 'https://www.astil.dev/'
    image_url = 'https://orindance.party/'
    image_width = 1001
    
    thumbnail_height = 1002
    thumbnail_proxy_url = 'https://www.astil.dev/'
    thumbnail_url = 'https://orindance.party/'
    thumbnail_width = 1003
    
    video_height = 1004
    video_proxy_url = 'https://www.astil.dev/'
    video_url = 'https://orindance.party/'
    video_width = 1005
    
    data = {
        'image': {
            'height': image_height,
            'proxy_url': image_proxy_url,
            'url': image_url,
            'width': image_width,
        },
        'thumbnail': {
            'height': thumbnail_height,
            'proxy_url': thumbnail_proxy_url,
            'url': thumbnail_url,
            'width': thumbnail_width,
        },
        'video': {
            'height': video_height,
            'proxy_url': video_proxy_url,
            'url': video_url,
            'width': video_width,
        },
    }
    
    embed = Embed()
    output = embed._update_sizes(data)
    vampytest.assert_eq(output, 1)
        
    vampytest.assert_is_not(embed.image, None)
    vampytest.assert_is_not(embed.thumbnail, None)
    vampytest.assert_is_not(embed.video, None)
    
    vampytest.assert_eq(embed.image.height, image_height)
    vampytest.assert_eq(embed.image.proxy_url, image_proxy_url)
    vampytest.assert_eq(embed.image.url, image_url)
    vampytest.assert_eq(embed.image.width, image_width)
    
    vampytest.assert_eq(embed.thumbnail.height, thumbnail_height)
    vampytest.assert_eq(embed.thumbnail.proxy_url, thumbnail_proxy_url)
    vampytest.assert_eq(embed.thumbnail.url, thumbnail_url)
    vampytest.assert_eq(embed.thumbnail.width, thumbnail_width)
    
    vampytest.assert_eq(embed.video.height, video_height)
    vampytest.assert_eq(embed.video.proxy_url, video_proxy_url)
    vampytest.assert_eq(embed.video.url, video_url)
    vampytest.assert_eq(embed.video.width, video_width)
    

def test__Embed__set_sises__all_change():
    """
    Tests whether ``Embed._set_sizes`` works as intended.
    
    Case: All changed.
    """
    image_height = 1000
    image_proxy_url = 'https://www.astil.dev/'
    image_url = 'https://orindance.party/'
    image_width = 1001
    
    thumbnail_height = 1002
    thumbnail_proxy_url = 'https://www.astil.dev/'
    thumbnail_url = 'https://orindance.party/'
    thumbnail_width = 1003
    
    video_height = 1004
    video_proxy_url = 'https://www.astil.dev/'
    video_url = 'https://orindance.party/'
    video_width = 1005
    
    data = {
        'image': {
            'height': image_height,
            'proxy_url': image_proxy_url,
            'url': image_url,
            'width': image_width,
        },
        'thumbnail': {
            'height': thumbnail_height,
            'proxy_url': thumbnail_proxy_url,
            'url': thumbnail_url,
            'width': thumbnail_width,
        },
        'video': {
            'height': video_height,
            'proxy_url': video_proxy_url,
            'url': video_url,
            'width': video_width,
        },
    }
    
    embed = Embed()
    embed._set_sizes(data)
    
    vampytest.assert_is_not(embed.image, None)
    vampytest.assert_is_not(embed.thumbnail, None)
    vampytest.assert_is_not(embed.video, None)
    
    vampytest.assert_eq(embed.image.height, image_height)
    vampytest.assert_eq(embed.image.proxy_url, image_proxy_url)
    vampytest.assert_eq(embed.image.url, image_url)
    vampytest.assert_eq(embed.image.width, image_width)
    
    vampytest.assert_eq(embed.thumbnail.height, thumbnail_height)
    vampytest.assert_eq(embed.thumbnail.proxy_url, thumbnail_proxy_url)
    vampytest.assert_eq(embed.thumbnail.url, thumbnail_url)
    vampytest.assert_eq(embed.thumbnail.width, thumbnail_width)
    
    vampytest.assert_eq(embed.video.height, video_height)
    vampytest.assert_eq(embed.video.proxy_url, video_proxy_url)
    vampytest.assert_eq(embed.video.url, video_url)
    vampytest.assert_eq(embed.video.width, video_width)
