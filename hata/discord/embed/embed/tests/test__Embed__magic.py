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
from ..flags import EmbedFlag
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
    yield {'flags': EmbedFlag(3)}, False
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
    flags = EmbedFlag(3)
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
        flags = flags,
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
    flags = EmbedFlag(3)
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
        flags = flags,
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


def _iter_options__eq():
    author = EmbedAuthor('author name')
    color = Color(123)
    description = 'embed description'
    embed_type = EmbedType.video
    fields = [EmbedField('komeiji', 'koishi'), EmbedField('komeiji', 'satori', inline = True)]
    flags = EmbedFlag(3)
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
        'flags': flags,
        'footer': footer,
        'image': image,
        'provider': provider,
        'thumbnail': thumbnail,
        'timestamp': timestamp,
        'title': title,
        'url': url,
        'video': video,
    }
    
    yield (
        keyword_parameters,
        keyword_parameters,
        True,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'author': EmbedAuthor('author derp'),
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'color': Color(124),
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'description': 'embed derp',
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'embed_type': EmbedType.gifv,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'fields': [EmbedField('komeiji', 'kokoro')],
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'flags': EmbedFlag(5),
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'footer': EmbedFooter('footer derp'),
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'image': EmbedImage('attachment://image_what'),
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'provider': EmbedProvider('provider derp'),
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'thumbnail': EmbedThumbnail('attachment://thumbnail_what'),
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'timestamp': DateTime(2016, 5, 4, tzinfo = TimeZone.utc),
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'title': 'embed derp',
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'url': 'https://www.astil.dev/project/hata/',
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'video': EmbedVideo('attachment://video_what'),
        },
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__Embed__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``Embed.__eq__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters_0 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    keyword_parameters_1 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : `bool`
    """
    embed_0 = Embed(**keyword_parameters_0)
    embed_1 = Embed(**keyword_parameters_1)
    
    output = embed_0 == embed_1
    vampytest.assert_instance(output, bool)
    return output
