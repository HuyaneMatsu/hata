import vampytest

from ...embed_author import EmbedAuthor
from ...embed_field import EmbedField
from ...embed_footer import EmbedFooter
from ...embed_image import EmbedImage
from ...embed_thumbnail import EmbedThumbnail

from ..embed import Embed


def test__Embed__add_author():
    """
    Tests whether ``Embed.add_author`` works as intended.
    """
    icon_url = 'attachment://orin.png'
    text = 'orin'
    url = 'https://orindance.party/'
    
    embed = Embed()
    output = embed.add_author(text, icon_url, url)
    
    vampytest.assert_eq(embed, output)
    vampytest.assert_eq(embed.author, EmbedAuthor(text, icon_url, url))


def test__Embed__add_field__0():
    """
    Tests whether ``Embed.add_field`` works as intended.
    
    Case: No fields.
    """
    field_0 = EmbedField('komeiji', 'satori', inline = True)
    
    embed = Embed()
    output = embed.add_field(field_0.name, field_0.value, field_0.inline)
    
    vampytest.assert_is(output, embed)
    vampytest.assert_eq(embed.fields, [field_0])


def test__Embed__add_field__1():
    """
    Tests whether ``Embed.add_field`` works as intended.
    
    Case: Fields exists.
    """
    field_0 = EmbedField('komeiji', 'koishi')
    field_1 = EmbedField('komeiji', 'satori', inline = True)
    
    embed = Embed(fields = [field_0])
    output = embed.add_field(field_1.name, field_1.value, field_1.inline)
    
    vampytest.assert_is(output, embed)
    vampytest.assert_eq(embed.fields, [field_0, field_1])


def test__Embed__insert_field__0():
    """
    Tests whether ``Embed.insert_field`` works as intended.
    
    Case: No fields.
    """
    field_0 = EmbedField('komeiji', 'satori', inline = True)
    
    embed = Embed()
    output = embed.insert_field(0, field_0.name, field_0.value, field_0.inline)
    
    vampytest.assert_is(output, embed)
    vampytest.assert_eq(embed.fields, [field_0])


def test__Embed__insert_field__1():
    """
    Tests whether ``Embed.insert_field`` works as intended.
    
    Case: Fields exists.
    """
    field_0 = EmbedField('komeiji', 'koishi')
    field_1 = EmbedField('komeiji', 'satori', inline = True)
    
    embed = Embed(fields = [field_0])
    output = embed.insert_field(0, field_1.name, field_1.value, field_1.inline)
    
    vampytest.assert_is(output, embed)
    vampytest.assert_eq(embed.fields, [field_1, field_0])


def test__Embed__get_field__0():
    """
    Tests whether ``Embed.get_field`` works as intended.
    
    Case: `IndexError`.
    """
    field_0 = EmbedField('komeiji', 'satori', inline = True)
    
    for input_value, index in (
        (None, 0),
        (None, 2),
        ([field_0], 2),
    ):
        embed = Embed(fields = input_value)
        
        with vampytest.assert_raises(IndexError):
            embed.get_field(index)


def test__Embed__get_field__1():
    """
    Tests whether ``Embed.get_field`` works as intended.
    
    Case: passing.
    """
    field_0 = EmbedField('komeiji', 'koishi')
    field_1 = EmbedField('komeiji', 'satori', inline = True)
    
    embed = Embed(fields = [field_0, field_1])
    
    for index, expected_output in (
        (0, field_0),
        (1, field_1),
        (-2, field_0),
    ):
        output = embed.get_field(index)
        vampytest.assert_eq(output, expected_output)


def test__Embed__append_field():
    """
    Tests whether ``Embed.append_field`` works as intended.
    """
    field_0 = EmbedField('komeiji', 'koishi')
    field_1 = EmbedField('komeiji', 'satori', inline = True)
    
    for input_field, input_fields, expected_fields in (
        (field_1, None, [field_1]),
        (field_0, [field_0], [field_0, field_0]),
        (field_1, [field_0], [field_0, field_1]),
    ):
        embed = Embed(fields = input_fields)
        embed.append_field(input_field)
        vampytest.assert_eq(embed.fields, expected_fields)


def test__Embed__set_field__0():
    """
    Tests whether ``Embed.set_field`` works as intended.
    
    Case: `IndexError`.
    """
    field_0 = EmbedField('komeiji', 'satori', inline = True)
    
    for input_fields, index in (
        (None, 0),
        (None, 2),
        ([field_0], 2),
    ):
        embed = Embed(fields = input_fields)
        
        with vampytest.assert_raises(IndexError):
            embed.set_field(index, field_0)


def test__Embed__set_field__1():
    """
    Tests whether ``Embed.set_field`` works as intended.
    
    Case: passing.
    """
    field_0 = EmbedField('komeiji', 'koishi')
    field_1 = EmbedField('komeiji', 'satori', inline = True)
    
    for index, input_field, expected_fields in (
        (0, field_1, [field_1, field_1]),
        (1, field_0, [field_0, field_0]),
        (-2, field_1, [field_1, field_1]),
    ):
        embed = Embed(fields = [field_0, field_1])
        embed.set_field(index, input_field)
        vampytest.assert_eq(embed.fields, expected_fields)


def test__Embed__del_field__0():
    """
    Tests whether ``Embed.del_field`` works as intended.
    
    Case: `IndexError`.
    """
    field_0 = EmbedField('komeiji', 'satori', inline = True)
    
    for input_value, index in (
        (None, 0),
        (None, 2),
        ([field_0], 2),
    ):
        embed = Embed(fields = input_value)
        
        with vampytest.assert_raises(IndexError):
            embed.del_field(index)


def test__Embed__del_field__1():
    """
    Tests whether ``Embed.del_field`` works as intended.
    
    Case: passing.
    """
    field_0 = EmbedField('komeiji', 'koishi')
    field_1 = EmbedField('komeiji', 'satori', inline = True)
    
    for index, expected_fields in (
        (0, [field_1]),
        (1, [field_0]),
        (-2, [field_1]),
    ):
        embed = Embed(fields = [field_0, field_1])
        
        embed.del_field(index)
        vampytest.assert_eq(embed.fields, expected_fields)


def test__Embed__remove_field():
    """
    Asserts whether ``Embed.remove_field`` and ``Embed.del_field`` are the same.
    """
    vampytest.assert_eq(Embed.remove_field, Embed.del_field)


def test__Embed__add_footer():
    """
    Tests whether ``Embed.add_footer`` works as intended.
    """
    icon_url = 'attachment://orin.png'
    text = 'orin'
    
    embed = Embed()
    output = embed.add_footer(text, icon_url)
    
    vampytest.assert_eq(embed, output)
    vampytest.assert_eq(embed.footer, EmbedFooter(text, icon_url))


def test__Embed__add_image():
    """
    Tests whether ``Embed.add_image`` works as intended.
    """
    url = 'attachment://orin.png'
    
    embed = Embed()
    output = embed.add_image(url)
    
    vampytest.assert_eq(embed, output)
    vampytest.assert_eq(embed.image, EmbedImage(url))


def test__Embed__add_thumbnail():
    """
    Tests whether ``Embed.add_thumbnail`` works as intended.
    """
    url = 'attachment://orin.png'
    
    embed = Embed()
    output = embed.add_thumbnail(url)
    
    vampytest.assert_eq(embed, output)
    vampytest.assert_eq(embed.thumbnail, EmbedThumbnail(url))
