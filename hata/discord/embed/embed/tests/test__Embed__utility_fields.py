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


def test__Embed__add_field__none():
    """
    Tests whether ``Embed.add_field`` works as intended.
    
    Case: No fields.
    """
    field_0 = EmbedField('komeiji', 'satori', inline = True)
    
    embed = Embed()
    output = embed.add_field(field_0.name, field_0.value, field_0.inline)
    
    vampytest.assert_is(output, embed)
    vampytest.assert_eq(embed.fields, [field_0])


def test__Embed__add_field__has():
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


def test__Embed__insert_field__none():
    """
    Tests whether ``Embed.insert_field`` works as intended.
    
    Case: No fields.
    """
    field_0 = EmbedField('komeiji', 'satori', inline = True)
    
    embed = Embed()
    output = embed.insert_field(0, field_0.name, field_0.value, field_0.inline)
    
    vampytest.assert_is(output, embed)
    vampytest.assert_eq(embed.fields, [field_0])


def test__Embed__insert_field__has():
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


def _iter_options__get_field__passing():
    field_0 = EmbedField('komeiji', 'koishi')
    field_1 = EmbedField('komeiji', 'satori', inline = True)
    
    yield [field_0, field_1], 0, field_0
    yield [field_0, field_1], 1, field_1
    yield [field_0, field_1], -2, field_0


def _iter_options__get_field__index_error():
    field_0 = EmbedField('komeiji', 'satori', inline = True)
    
    yield None, 0
    yield None, -1
    yield None, 2
    yield [field_0], 2


@vampytest._(vampytest.call_from(_iter_options__get_field__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__get_field__index_error()).raising(IndexError))
def test__Embed__get_field(input_fields, index):
    """
    Tests whether ``Embed.get_field`` works as intended.
    
    Parameters
    ----------
    input_fields : `None | list<EmbedField>`
        Fields to create the embed with.
    index : `int`
        The index to get the field at.
    
    Returns
    -------
    output : ``EmbedField``
    
    Raising
    -------
    IndexError
    """
    embed = Embed(fields = input_fields)
    output = embed.get_field(index)
    vampytest.assert_instance(output, EmbedField)
    return output


def _iter_options__append_field():
    field_0 = EmbedField('komeiji', 'koishi')
    field_1 = EmbedField('komeiji', 'satori', inline = True)
    
    yield None, field_1, [field_1]
    yield [field_0], field_0, [field_0, field_0]
    yield [field_0], field_1, [field_0, field_1]


@vampytest._(vampytest.call_from(_iter_options__append_field()).returning_last())
def test__Embed__append_field(input_fields, field):
    """
    Tests whether ``Embed.append_field`` works as intended.
    
    Parameters
    ----------
    input_fields : `None | list<EmbedField>`
        Fields to create the embed with.
    field : ``EmbedField``
        Field to add.
    
    Returns
    -------
    output : `None | list<EmbedField>`
    """
    embed = Embed(fields = input_fields)
    embed.append_field(field)
    return embed.fields


def _iter_options__set_field__passing():
    field_0 = EmbedField('komeiji', 'koishi')
    field_1 = EmbedField('komeiji', 'satori', inline = True)
    
    yield [field_0, field_1], 0, field_1, [field_1, field_1]
    yield [field_0, field_1], 1, field_0, [field_0, field_0]
    yield [field_0, field_1], -2, field_1, [field_1, field_1]


def _iter_options__set_field__index_error():
    field_0 = EmbedField('komeiji', 'koishi')
    
    yield None, 0, field_0
    yield None, 2, field_0,
    yield [field_0], 2, field_0


@vampytest._(vampytest.call_from(_iter_options__set_field__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__set_field__index_error()).raising(IndexError))
def test__Embed__set_field(input_fields, index, field):
    """
    Tests whether ``Embed.set_field`` works as intended.
    
    Parameters
    ----------
    input_fields : `None | list<EmbedField>`
        Fields to create the embed with.
    index : `int`
        The index to set the field at.
    field : ``EmbedField``
        Field to set.
    
    Returns
    -------
    fields : `None | list<EmbedField>`
    
    Raises
    ------
    IndexError
    """
    embed = Embed(fields = input_fields)
    embed.set_field(index, field)
    return embed.fields


def _iter_options__del_field_passing():
    field_0 = EmbedField('komeiji', 'koishi')
    field_1 = EmbedField('komeiji', 'satori', inline = True)
    
    yield [field_0, field_1], 0, [field_1]
    yield [field_0, field_1], 1, [field_0]
    yield [field_0, field_1], -2, [field_1]
    

def _iter_options__del_field__index_error():
    field_0 = EmbedField('komeiji', 'satori', inline = True)
    
    yield None, 0
    yield None, 2
    yield [field_0], 2


@vampytest._(vampytest.call_from(_iter_options__del_field_passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__del_field__index_error()).raising(IndexError))
def test__Embed__del_field(input_fields, index):
    """
    Tests whether ``Embed.del_field`` works as intended.
    
    Parameters
    ----------
    input_fields : `None | list<EmbedField>`
        Fields to create the embed with.
    index : `int`
        The index to set the field at.
    
    Returns
    -------
    fields : `None | list<EmbedField>`
    
    Raises
    ------
    IndexError
    """
    embed = Embed(fields = input_fields)
    embed.del_field(index)
    return embed.fields


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
