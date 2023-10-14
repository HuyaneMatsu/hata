from datetime import datetime as DateTime

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
    timestamp = DateTime(2016, 5, 5)
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


def test__Embed__bool__0():
    """
    Tests whether ``Embed.__bool__`` works as intended.
    
    Case: Empty embed.
    """
    embed = Embed()
    vampytest.assert_false(embed)


def test__Embed__bool__1():
    """
    Tests whether ``Embed.__bool__`` works as intended.
    
    Case: true embed.
    """
    for field_name, field_value in (
        ('author', EmbedAuthor('author name')),
        ('color', Color(123)),
        ('description', 'embed description'),
        # ('embed_type', EmbedType.video), # not applicable for type
        ('fields', [EmbedField('komeiji', 'koishi'), EmbedField('komeiji', 'satori', inline = True)]),
        ('footer', EmbedFooter('footer text')),
        ('image', EmbedImage('attachment://image')),
        ('provider', EmbedProvider('provider name')),
        ('thumbnail', EmbedThumbnail('attachment://thumbnail')),
        ('timestamp', DateTime(2016, 5, 5)),
        ('title', 'embed title'),
        ('url', 'https://orindance.party/'),
        ('video', EmbedVideo('attachment://video')),
    ):
        embed = Embed(**{field_name: field_value})
        vampytest.assert_true(embed)


def test__Embed__bool__2():
    """
    Tests whether ``Embed.__bool__`` works as intended.
    
    Case: false embed.
    """
    for field_name, field_value in (
        ('author', EmbedAuthor()),
        ('embed_type', EmbedType.video),
        ('fields', [EmbedField(), EmbedField(inline = True)]),
        ('footer', EmbedFooter()),
        ('image', EmbedImage()),
        ('provider', EmbedProvider()),
        ('thumbnail', EmbedThumbnail()),
        ('video', EmbedVideo()),
    ):
        embed = Embed(**{field_name: field_value})
        vampytest.assert_false(embed)


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
    timestamp = DateTime(2016, 5, 5)
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
    timestamp = DateTime(2016, 5, 5)
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
    timestamp = DateTime(2016, 5, 5)
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
        ('timestamp', DateTime(2016, 5, 4)),
        ('title', 'embed derp'),
        ('url', 'https://www.astil.dev/project/hata/'),
        ('video', EmbedVideo('attachment://video_what')),
    ):
        test_embed = Embed(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(embed, test_embed)
