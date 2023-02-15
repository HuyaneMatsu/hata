import vampytest

from ..embed_base import EmbedAuthor, EmbedProvider
from ..embed import Embed


def test__Embed__iter_contents__0():
    """
    Tests whether ``Embed.iter_contents`` works as intended.
    
    Case: All contents.
    """
    embed_title = 'orin'
    embed_author_name = 'riverside'
    embed_description = 'relief'
    embed_field_0_name = 'shiki'
    embed_field_0_value = 'yukari'
    embed_field_1_name = 'ran'
    embed_field_1_value = 'chen'
    embed_footer_text = 'okina'
    embed_provider_name = 'hecatia'
    
    embed = Embed(title = embed_title, description = embed_description)
    embed.author = EmbedAuthor(embed_author_name)
    embed.add_field(embed_field_0_name, embed_field_0_value)
    embed.add_field(embed_field_1_name, embed_field_1_value)
    embed.add_footer(embed_footer_text)
    embed.provider = EmbedProvider(embed_provider_name)
    
    contents = {
        embed_title, embed_author_name, embed_description, embed_field_0_name, embed_field_0_value, embed_field_1_name,
        embed_field_1_value, embed_footer_text, embed_provider_name
    }
    
    vampytest.assert_eq({*embed.iter_contents()}, contents)


def test__Embed__iter_contents__1():
    """
    Tests whether ``Embed.iter_contents`` works as intended.
    
    Case: No contents.
    """
    embed = Embed()
    vampytest.assert_eq({*embed.iter_contents()}, set())


def test__Embed__contents__0():
    """
    Tests whether ``Embed.contents`` works as intended.
    
    Case: All contents.
    """
    embed_title = 'orin'
    embed_author_name = 'riverside'
    embed_description = 'relief'
    embed_field_0_name = 'shiki'
    embed_field_0_value = 'yukari'
    embed_field_1_name = 'ran'
    embed_field_1_value = 'chen'
    embed_footer_text = 'okina'
    embed_provider_name = 'hecatia'
    
    embed = Embed(title = embed_title, description = embed_description)
    embed.author = EmbedAuthor(embed_author_name)
    embed.add_field(embed_field_0_name, embed_field_0_value)
    embed.add_field(embed_field_1_name, embed_field_1_value)
    embed.add_footer(embed_footer_text)
    embed.provider = EmbedProvider(embed_provider_name)
    
    
    contents = {
        embed_title, embed_author_name, embed_description, embed_field_0_name, embed_field_0_value, embed_field_1_name,
        embed_field_1_value, embed_footer_text, embed_provider_name
    }
    
    output = embed.contents
    vampytest.assert_instance(output, list)
    vampytest.assert_eq({*output}, contents)


def test__Embed__contents__1():
    """
    Tests whether ``Embed.contents`` works as intended.
    
    Case: No contents.
    """
    embed = Embed()
    
    output = embed.contents
    vampytest.assert_instance(output, list)
    vampytest.assert_eq({*output}, set())
