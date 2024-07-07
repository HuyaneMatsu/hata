from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....color import Color

from ...embed_author import EmbedAuthor
from ...embed_field import EmbedField
from ...embed_footer import EmbedFooter
from ...embed_image import EmbedImage
from ...embed_provider import EmbedProvider
from ...embed_thumbnail import EmbedThumbnail
from ...embed_video import EmbedVideo

from ..embed import Embed
from ..preinstanced import EmbedType


def test__Embed__len():
    """
    Tests whether ``Embed.__len__`` works as intended.
    """
    embed_author_name = 'author name'
    embed_description = 'embed description'
    embed_field_0_name = 'komeiji'
    embed_field_0_value = 'koishi'
    embed_field_1_name = 'komeiji'
    embed_field_1_value = 'satori'
    embed_footer_text = 'footer text'
    embed_provider_name = 'provider name'
    embed_title = 'embed title'
    
    author = EmbedAuthor(embed_author_name)
    color = Color(123)
    description = embed_description
    embed_type = EmbedType.video
    fields = [
        EmbedField(embed_field_0_name, embed_field_0_value),
        EmbedField(embed_field_1_name, embed_field_1_value, inline = True),
    ]
    footer = EmbedFooter(embed_footer_text)
    image = EmbedImage('attachment://image')
    provider = EmbedProvider(embed_provider_name)
    thumbnail = EmbedThumbnail('attachment://thumbnail')
    timestamp = DateTime(2016, 5, 5, tzinfo = TimeZone.utc)
    title = embed_title
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
    
    expected_output = (
        len(embed_author_name) + len(embed_description) + len(embed_field_0_name) + len(embed_field_0_value) +
        len(embed_field_1_name) + len(embed_field_1_value) + len(embed_footer_text) + len(embed_provider_name) +
        len(embed_title)
    )
    
    output = len(embed)
    vampytest.assert_instance(output, int)
    vampytest.assert_eq(output, expected_output)



def _iter_options__bool():
    yield {}, False
    yield {'author': EmbedAuthor('author name')}, True
    yield {'color': Color(123)}, True
    yield {'description': 'embed description'}, True
    yield {'fields': [EmbedField('komeiji', 'koishi'), EmbedField('komeiji', 'satori', inline = True)]}, True
    yield {'footer': EmbedFooter('footer text')}, True
    yield {'image': EmbedImage('attachment://image')}, True
    yield {'provider': EmbedProvider('provider name')}, True
    yield {'thumbnail': EmbedThumbnail('attachment://thumbnail')}, True
    yield {'timestamp': DateTime(2016, 5, 5, tzinfo = TimeZone.utc)}, True
    yield {'title': 'embed title'}, True
    yield {'url': 'https://orindance.party/'}, True
    yield {'video': EmbedVideo('attachment://video')}, True

    yield {'embed_type': EmbedType.video}, False
    yield {'author': EmbedAuthor()}, False
    yield {'fields': [EmbedField(), EmbedField(inline = True)]}, False
    yield {'footer': EmbedFooter()}, False
    yield {'image': EmbedImage()}, False
    yield {'provider': EmbedProvider()}, False
    yield {'thumbnail': EmbedThumbnail()}, False
    yield {'video': EmbedVideo()}, False


@vampytest._(vampytest.call_from(_iter_options__bool()).returning_last())
def test__Embed__bool(keyword_parameters):
    """
    Tests whether ``Embed.__bool__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword Parameters to edit.
    
    Returns
    -------
    output : `bool`
    """
    embed = Embed(**keyword_parameters)
    output = bool(embed)
    vampytest.assert_instance(output, bool)
    return output


def test__Embed__repr():
    """
    Tests whether ``Embed.__repr__`` works as intended.
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
    
    vampytest.assert_instance(repr(embed), str)


def test__Embed__hash():
    """
    Tests whether ``Embed.__hash__`` works as intended.
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
        video = video,
    )
    
    vampytest.assert_instance(hash(embed), int)


def test__Embed__eq():
    """
    Tests whether ``Embed.__eq__`` works as intended.
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
    
    keyword_parameters = {
        'author': author,
        'color': color,
        'description': description,
        'embed_type': embed_type,
        'fields': fields,
        'footer': footer,
        'image': image,
        'provider': provider,
        'thumbnail': thumbnail,
        'timestamp': timestamp,
        'title': title,
        'url': url,
        'video': video,
    }

    embed = Embed(**keyword_parameters)
    
    vampytest.assert_eq(embed, embed)
    vampytest.assert_ne(embed, object())
    
    for field_name, field_value in (
        ('author', EmbedAuthor('author derp')),
        ('color', Color(124)),
        ('description', 'embed derp'),
        ('embed_type', EmbedType.gifv),
        ('fields', [EmbedField('komeiji', 'kokoro')]),
        ('footer', EmbedFooter('footer derp')),
        ('image', EmbedImage('attachment://image_what')),
        ('provider', EmbedProvider('provider derp')),
        ('thumbnail', EmbedThumbnail('attachment://thumbnail_what')),
        ('timestamp', DateTime(2016, 5, 4, tzinfo = TimeZone.utc)),
        ('title', 'embed derp'),
        ('url', 'https://www.astil.dev/project/hata/'),
        ('video', EmbedVideo('attachment://video_what')),
    ):
        test_embed = Embed(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(embed, test_embed)
