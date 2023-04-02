import vampytest

from ...embed import EmbedAuthor, Embed, EmbedField, EmbedFooter, EmbedProvider

from ..message import Message



def test__Message__iter_contents__0():
    """
    Tests whether ``Message.iter_contents`` works as intended.
    
    Case: All contents.
    """
    channel_id = 202302150000
    message_content = 'okuu'
    embed_0_title = 'orin'
    embed_0_author_name = 'riverside'
    embed_0_description = 'relief'
    embed_0_field_0_name = 'shiki'
    embed_0_field_0_value = 'yukari'
    embed_0_field_1_name = 'ran'
    embed_0_field_1_value = 'chen'
    embed_0_footer_text = 'okina'
    embed_0_provider_name = 'hecatia'
    embed_1_title = 'reimu'
    
    embed_0 = Embed(title = embed_0_title, description = embed_0_description)
    embed_0.author = EmbedAuthor(embed_0_author_name)
    embed_0.fields = [
        EmbedField(embed_0_field_0_name, embed_0_field_0_value),
        EmbedField(embed_0_field_1_name, embed_0_field_1_value),
    ]
    embed_0.footer = EmbedFooter(embed_0_footer_text)
    embed_0.provider = EmbedProvider(embed_0_provider_name)
    
    embed_1 = Embed(title = embed_1_title)
    
    message = Message.custom(channel_id = channel_id, content = message_content, embeds = [embed_0, embed_1])
    
    
    contents = {
        embed_0_title, embed_0_author_name, embed_0_description, embed_0_field_0_name, embed_0_field_0_value,
        embed_0_field_1_name, embed_0_field_1_value, embed_0_footer_text, embed_0_provider_name,
        message_content, embed_1_title
    }
    
    vampytest.assert_eq({*message.iter_contents()}, contents)


def test__Message__iter_contents__1():
    """
    Tests whether ``Embed.iter_contents`` works as intended.
    
    Case: No contents.
    """
    channel_id = 202302150001
    message = Message.custom(channel_id = channel_id)
    vampytest.assert_eq({*message.iter_contents()}, set())


def test__Message__contents__0():
    """
    Tests whether ``Message.contents`` works as intended.
    
    Case: All contents.
    """
    channel_id = 202302150002
    message_content = 'okuu'
    embed_0_title = 'orin'
    embed_0_author_name = 'riverside'
    embed_0_description = 'relief'
    embed_0_field_0_name = 'shiki'
    embed_0_field_0_value = 'yukari'
    embed_0_field_1_name = 'ran'
    embed_0_field_1_value = 'chen'
    embed_0_footer_text = 'okina'
    embed_0_provider_name = 'hecatia'
    embed_1_title = 'reimu'
    
    embed_0 = Embed(title = embed_0_title, description = embed_0_description)
    embed_0.author = EmbedAuthor(embed_0_author_name)
    embed_0.fields = [
        EmbedField(embed_0_field_0_name, embed_0_field_0_value),
        EmbedField(embed_0_field_1_name, embed_0_field_1_value),
    ]
    embed_0.footer = EmbedFooter(embed_0_footer_text)
    embed_0.provider = EmbedProvider(embed_0_provider_name)
    
    embed_1 = Embed(title = embed_1_title)
    
    message = Message.custom(channel_id = channel_id, content = message_content, embeds = [embed_0, embed_1])
    
    contents = {
        embed_0_title, embed_0_author_name, embed_0_description, embed_0_field_0_name, embed_0_field_0_value,
        embed_0_field_1_name, embed_0_field_1_value, embed_0_footer_text, embed_0_provider_name,
        message_content, embed_1_title
    }
    
    output = message.contents
    vampytest.assert_instance(output, list)
    vampytest.assert_eq({*output}, contents)


def test__Message__contents__1():
    """
    Tests whether ``Message.contents`` works as intended.
    
    Case: No contents.
    """
    channel_id = 202302150003
    message = Message.custom(channel_id = channel_id)
    
    output = message.contents
    vampytest.assert_instance(output, list)
    vampytest.assert_eq({*output}, set())
