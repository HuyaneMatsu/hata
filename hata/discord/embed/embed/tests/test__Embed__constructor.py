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


def _assert_fields_set(embed):
    """
    Asserts whether every field of the given embed are set.
    
    Parameters
    ----------
    embed : ``Embed``
    """
    vampytest.assert_instance(embed, Embed)
    vampytest.assert_instance(embed.author, EmbedAuthor, nullable = True)
    vampytest.assert_instance(embed.color, Color, nullable = True)
    vampytest.assert_instance(embed.description, str, nullable = True)
    vampytest.assert_instance(embed.fields, list, nullable = True)
    vampytest.assert_instance(embed.footer, EmbedFooter, nullable = True)
    vampytest.assert_instance(embed.image, EmbedImage, nullable = True)
    vampytest.assert_instance(embed.provider, EmbedProvider, nullable = True)
    vampytest.assert_instance(embed.thumbnail, EmbedThumbnail, nullable = True)
    vampytest.assert_instance(embed.timestamp, DateTime, nullable = True)
    vampytest.assert_instance(embed.title, str, nullable = True)
    vampytest.assert_instance(embed.type, EmbedType, nullable = True)
    vampytest.assert_instance(embed.url, str, nullable = True)
    vampytest.assert_instance(embed.video, EmbedVideo, nullable = True)


def test__Embed__new__no_fields():
    """
    Tests whether ``Embed.__new__`` works as intended.
    
    Case: No fields given.
    """
    embed = Embed()
    _assert_fields_set(embed)


def test__Embed__new__all_fields():
    """
    Tests whether ``Embed.__new__`` works as intended.
    
    Case: All fields given.
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


def test__Embed__new__conversion_check():
    """
    Tests whether ``Embed.__new__`` works as intended.
    
    Case: title & description conversion check.
    """
    description = 123
    title = 245
    
    embed = Embed(
        description = description,
        title = title,
    )
    _assert_fields_set(embed)
    
    vampytest.assert_eq(embed.description, str(description))
    vampytest.assert_eq(embed.title, str(title))
