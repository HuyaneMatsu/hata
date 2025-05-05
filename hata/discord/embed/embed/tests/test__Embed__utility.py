from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....color import Color
from ....guild import Guild
from ....user import GuildProfile, User

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

from .test__Embed__constructor import _assert_fields_set


def test__Embed__clear():
    """
    Tests whether ``Embed.clear`` works as intended.
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
    
    embed.clear()
    
    vampytest.assert_is(embed.author, None)
    vampytest.assert_is(embed.color, None)
    vampytest.assert_is(embed.description, None)
    vampytest.assert_is(embed.fields, None)
    vampytest.assert_eq(embed.flags, EmbedFlag())
    vampytest.assert_is(embed.footer, None)
    vampytest.assert_is(embed.image, None)
    vampytest.assert_is(embed.provider, None)
    vampytest.assert_is(embed.thumbnail, None)
    vampytest.assert_is(embed.timestamp, None)
    vampytest.assert_is(embed.title, None)
    vampytest.assert_is(embed.type, None)
    vampytest.assert_is(embed.url, None)
    vampytest.assert_is(embed.video, None)


def test__Embed__clean_copy():
    """
    Tests whether ``Embed.clean_copy`` works as intended.
    """
    guild_id = 202505030010
    guild = Guild.precreate(guild_id)
    
    user_0 = User.precreate(2023004010000, name = 'koishi')
    user_0.guild_profiles[202505030010] = GuildProfile(nick = 'koi')
    user_1 = User.precreate(2023004010001, name = 'satori')
    user_1.guild_profiles[202505030010] = GuildProfile(nick = 'sato')
    user_2 = User.precreate(2023004010002, name = 'reimu')
    user_2.guild_profiles[202505030010] = GuildProfile(nick = 'rei')
    user_3 = User.precreate(2023004010003, name = 'marisa')
    user_3.guild_profiles[202505030010] = GuildProfile(nick = 'mari')
    user_4 = User.precreate(2023004010004, name = 'sanae')
    user_4.guild_profiles[202505030010] = GuildProfile(nick = 'sana')
    user_5 = User.precreate(2023004010005, name = 'rin')
    user_5.guild_profiles[202505030010] = GuildProfile(nick = 'orin')
    user_6 = User.precreate(2023004010006, name = 'utsuho')
    user_6.guild_profiles[202505030010] = GuildProfile(nick = 'okuu')
    
    author = EmbedAuthor(user_0.mention)
    description = user_1.mention
    fields = [EmbedField(user_2.mention, user_3.mention, inline = True)]
    footer = EmbedFooter(user_4.mention)
    provider = EmbedProvider(user_5.mention)
    title = user_6.mention
    
    embed = Embed(
        author = author,
        description = description,
        fields = fields,
        footer = footer,
        provider = provider,
        title = title,
    )
    
    copy = embed.clean_copy(guild)
    _assert_fields_set(copy)
    vampytest.assert_is_not(embed, copy)
    
    vampytest.assert_eq(copy.author, EmbedAuthor(f'@{user_0.name_at(guild)}'))
    vampytest.assert_eq(copy.description, f'@{user_1.name_at(guild)}')
    vampytest.assert_eq(
        copy.fields,
        [
            EmbedField(f'@{user_2.name_at(guild)}', f'@{user_3.name_at(guild)}', inline = True),
        ],
    )
    vampytest.assert_eq(copy.footer, EmbedFooter(f'@{user_4.name_at(guild)}'))
    vampytest.assert_eq(copy.provider, EmbedProvider(f'@{user_5.name_at(guild)}'))
    vampytest.assert_eq(copy.title, f'@{user_6.name_at(guild)}')


def test__Embed__copy():
    """
    Tests whether ``Embed.copy`` works as intended.
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
    
    copy = embed.copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(embed, copy)
    
    vampytest.assert_eq(embed, copy)


def test__Embed__copy_with__no_fields():
    """
    Tests whether ``Embed.copy_with`` works as intended.
    
    Case: No fields given.
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
    
    copy = embed.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_is_not(embed, copy)
    
    vampytest.assert_eq(embed, copy)


def test__Embed__copy_with__all_fields():
    """
    Tests whether ``Embed.copy_with`` works as intended.
    
    Case: All fields given.
    """
    old_author = EmbedAuthor('author name')
    old_color = Color(123)
    old_description = 'embed description'
    old_embed_type = EmbedType.video
    old_fields = [EmbedField('komeiji', 'koishi'), EmbedField('komeiji', 'satori', inline = True)]
    old_flags = EmbedFlag(3)
    old_footer = EmbedFooter('footer text')
    old_image = EmbedImage('attachment://image')
    old_provider = EmbedProvider('provider name')
    old_thumbnail = EmbedThumbnail('attachment://thumbnail')
    old_timestamp = DateTime(2016, 5, 5, tzinfo = TimeZone.utc)
    old_title = 'embed title'
    old_url = 'https://orindance.party/'
    old_video = EmbedVideo('attachment://video')
    
    new_author = EmbedAuthor('author derp')
    new_color = Color(124)
    new_description = 'embed derp'
    new_embed_type = EmbedType.gifv
    new_fields = [EmbedField('komeiji', 'yukari', inline = True)]
    new_flags = EmbedFlag(5)
    new_footer = EmbedFooter('footer derp')
    new_image = EmbedImage('attachment://image_hello')
    new_provider = EmbedProvider('provider derp')
    new_thumbnail = EmbedThumbnail('attachment://thumbnail_hello')
    new_timestamp = DateTime(2016, 5, 4, tzinfo = TimeZone.utc)
    new_title = 'embed hello'
    new_url = 'https://www.astil.dev/project/hata/'
    new_video = EmbedVideo('attachment://video_hello')
    
    embed = Embed(
        author = old_author,
        color = old_color,
        description = old_description,
        embed_type = old_embed_type,
        fields = old_fields,
        flags = old_flags,
        footer = old_footer,
        image = old_image,
        provider = old_provider,
        thumbnail = old_thumbnail,
        timestamp = old_timestamp,
        title = old_title,
        url = old_url,
        video = old_video,
    )
    
    copy = embed.copy_with(
        author = new_author,
        color = new_color,
        description = new_description,
        embed_type = new_embed_type,
        fields = new_fields,
        flags = new_flags,
        footer = new_footer,
        image = new_image,
        provider = new_provider,
        thumbnail = new_thumbnail,
        timestamp = new_timestamp,
        title = new_title,
        url = new_url,
        video = new_video,
    )
    _assert_fields_set(copy)
    vampytest.assert_is_not(embed, copy)
    
    vampytest.assert_eq(copy.author, new_author)
    vampytest.assert_eq(copy.color, new_color)
    vampytest.assert_eq(copy.description, new_description)
    vampytest.assert_eq(copy.fields, new_fields)
    vampytest.assert_eq(copy.flags, new_flags)
    vampytest.assert_eq(copy.footer, new_footer)
    vampytest.assert_eq(copy.image, new_image)
    vampytest.assert_eq(copy.provider, new_provider)
    vampytest.assert_eq(copy.thumbnail, new_thumbnail)
    vampytest.assert_eq(copy.timestamp, new_timestamp)
    vampytest.assert_eq(copy.title, new_title)
    vampytest.assert_eq(copy.type, new_embed_type)
    vampytest.assert_eq(copy.url, new_url)
    vampytest.assert_eq(copy.video, new_video)


def test__Embed__iter_contents__all():
    """
    Tests whether ``Embed.iter_contents`` works as intended.
    
    Case: All contents.
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
    
    expected_output = {
        embed_author_name, embed_description, embed_field_0_name, embed_field_0_value, embed_field_1_name,
        embed_field_1_value, embed_footer_text, embed_provider_name, embed_title
    }
    
    vampytest.assert_eq({*embed.iter_contents()}, expected_output)


def test__Embed__iter_contents__none():
    """
    Tests whether ``Embed.iter_contents`` works as intended.
    
    Case: No contents.
    """
    embed = Embed()
    vampytest.assert_eq({*embed.iter_contents()}, set())


def test__Embed__contents__all():
    """
    Tests whether ``Embed.contents`` works as intended.
    
    Case: All contents.
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
    
    expected_output = {
        embed_author_name, embed_description, embed_field_0_name, embed_field_0_value, embed_field_1_name,
        embed_field_1_value, embed_footer_text, embed_provider_name, embed_title
    }
    
    output = embed.contents
    vampytest.assert_instance(output, list)
    vampytest.assert_eq({*output}, expected_output)


def test__Embed__contents__none():
    """
    Tests whether ``Embed.contents`` works as intended.
    
    Case: No contents.
    """
    embed = Embed()
    
    output = embed.contents
    vampytest.assert_instance(output, list)
    vampytest.assert_eq({*output}, set())



def _iter_options__iter_fields():
    field_0 = EmbedField('komeiji', 'koishi')
    field_1 = EmbedField('komeiji', 'satori', inline = True)
    
    yield None, []
    yield [field_0], [field_0]
    yield [field_0, field_1], [field_0, field_1]
    

@vampytest._(vampytest.call_from(_iter_options__iter_fields()).returning_last())
def test__Embed__iter_fields(input_fields):
    """
    Tests whether ``Embed.iter_fields`` works as intended.
    
    Parameters
    ----------
    input_fields : `dict<str, object>`
        Fields to create the embed with.
    
    Returns
    -------
    output : `list<EmbedField>`
    """
    embed = Embed(fields = input_fields)
    return [*embed.iter_fields()]


def test__Embed__get_short_repr():
    """
    Tests whether ``Embed.get_short_repr`` works as intended.
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
    
    vampytest.assert_instance(embed.get_short_repr(), str)
