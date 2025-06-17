import vampytest

from ...sticker import Sticker

from ..sticker_pack import StickerPack

from .test__StickerPack__constructor import _assert_fields_set


def test__StickerPack__copy():
    """
    Tests whether ``StickerPack.copy`` works as intended.
    """
    banner_id = 202201060053
    cover_sticker_id = 202201060054
    description = 'Kodemari'
    name = 'Koruri'
    sku_id = 202201060055
    stickers = [Sticker.precreate(202201060056), Sticker.precreate(202201060057)]
    
    sticker_pack = StickerPack(
        banner_id = banner_id,
        cover_sticker_id = cover_sticker_id,
        description = description,
        name = name,
        sku_id = sku_id,
        stickers = stickers,
    )
    
    copy = sticker_pack.copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(sticker_pack, copy)
    
    vampytest.assert_eq(sticker_pack, copy)


def test__StickerPack__copy_with__no_fields():
    """
    Tests whether ``StickerPack.copy_with`` works as intended.
    
    Case: No fields given.
    """
    banner_id = 202201060058
    cover_sticker_id = 202201060059
    description = 'Kodemari'
    name = 'Koruri'
    sku_id = 202201060060
    stickers = [Sticker.precreate(202201060061), Sticker.precreate(202201060062)]
    
    sticker_pack = StickerPack(
        banner_id = banner_id,
        cover_sticker_id = cover_sticker_id,
        description = description,
        name = name,
        sku_id = sku_id,
        stickers = stickers,
    )
    
    copy = sticker_pack.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_is_not(sticker_pack, copy)
    
    vampytest.assert_eq(sticker_pack, copy)


def test__StickerPack__copy_with__all_fields():
    """
    Tests whether ``StickerPack.copy_with`` works as intended.
    
    Case: All fields given.
    """
    old_banner_id = 202201060063
    old_cover_sticker_id = 202201060064
    old_description = 'Kodemari'
    old_name = 'Koruri'
    old_sku_id = 202201060065
    old_stickers = [Sticker.precreate(202201060066), Sticker.precreate(202201060067)]
    
    new_banner_id = 202201060068
    new_cover_sticker_id = 202201060069
    new_description = 'Komeiji'
    new_name = 'Koishi'
    new_sku_id = 202201060070
    new_stickers = [Sticker.precreate(202201060071)]
    
    sticker_pack = StickerPack(
        banner_id = old_banner_id,
        cover_sticker_id = old_cover_sticker_id,
        description = old_description,
        name = old_name,
        sku_id = old_sku_id,
        stickers = old_stickers,
    )
    
    copy = sticker_pack.copy_with(
        banner_id = new_banner_id,
        cover_sticker_id = new_cover_sticker_id,
        description = new_description,
        name = new_name,
        sku_id = new_sku_id,
        stickers = new_stickers
    )
    _assert_fields_set(copy)
    vampytest.assert_is_not(sticker_pack, copy)
    
    vampytest.assert_eq(copy.banner_id, new_banner_id)
    vampytest.assert_eq(copy.cover_sticker_id, new_cover_sticker_id)
    vampytest.assert_eq(copy.description, new_description)
    vampytest.assert_eq(copy.name, new_name)
    vampytest.assert_eq(copy.sku_id, new_sku_id)
    vampytest.assert_eq(copy.stickers, frozenset(new_stickers))


def test__StickerPack__partial():
    """
    Tests whether ``StickerPack.partial`` works as intended.
    """
    sticker_pack_id = 202201060072
    
    sticker_pack = StickerPack.precreate(sticker_pack_id)
    vampytest.assert_false(sticker_pack.partial)
    
    sticker_pack = StickerPack()
    vampytest.assert_true(sticker_pack.partial)


def _iter_options__iter_stickers():
    sticker_0 = Sticker.precreate(202201060073)
    sticker_1 = Sticker.precreate(202201060074)
    
    yield None, set()
    yield [sticker_0], {sticker_0}
    yield [sticker_0, sticker_1], {sticker_0, sticker_1}


@vampytest._(vampytest.call_from(_iter_options__iter_stickers()).returning_last())
def test__StickerPack__iter_stickers(stickers):
    """
    Tests whether ``StickerPack.iter_stickers`` works as intended.
    
    Parameters
    ----------
    stickers : ``None | list<Sticker>``
        Stickers to create the sticker pack with.
    
    Returns
    -------
    output : ``set<Sticker>``
    """
    sticker_pack = StickerPack(stickers = stickers)
    output = {*sticker_pack.iter_stickers()}
    
    for element in output:
        vampytest.assert_instance(element, Sticker)
    
    return output


def _iter_options__has_sticker():
    sticker_0 = Sticker.precreate(202201060075)
    sticker_1 = Sticker.precreate(202201060076)
    
    yield None, sticker_0, False
    yield [sticker_0], sticker_0, True
    yield [sticker_1], sticker_0, False


@vampytest._(vampytest.call_from(_iter_options__has_sticker()).returning_last())
def test__StickerPack__has_sticker(stickers, sticker):
    """
    Tests whether ``StickerPack.has_sticker` works as intended.
    Parameters
    ----------
    stickers : ``None | list<Sticker>``
        Stickers to create the sticker pack with.
    
    sticker : ``Sticker``
        Sticker to test with.
    
    Returns
    -------
    output : `bool`
    """
    sticker_pack = StickerPack(stickers = stickers)
    output = sticker_pack.has_sticker(sticker)
    vampytest.assert_instance(output, bool)
    return output


def _iter_options__banner_url():
    yield 202506010012, 0, False
    yield 202506010014, 202506010015, True


@vampytest._(vampytest.call_from(_iter_options__banner_url()).returning_last())
def test__StickerPack__banner_url(sticker_pack_id, banner_id):
    """
    Tests whether ``StickerPack.banner_url`` works as intended.
    
    Parameters
    ----------
    sticker_pack_id : `int`
        Identifier to create sticker pack with.
    
    banner_id : `int`
        Banner identifier to create the sticker pack with.
    
    Returns
    -------
    has_banner_url : `bool`
    """
    sticker_pack = StickerPack.precreate(
        sticker_pack_id,
        banner_id = banner_id,
    )
    
    output = sticker_pack.banner_url
    vampytest.assert_instance(output, str, nullable = True)
    return (output is not None)


def _iter_options__banner_url_as():
    yield 202506010016, 0, {'ext': 'webp', 'size': 128}, False
    yield 202506010018, 202506010019, {'ext': 'webp', 'size': 128}, True


@vampytest._(vampytest.call_from(_iter_options__banner_url_as()).returning_last())
def test__StickerPack__banner_url_as(sticker_pack_id, banner_id, keyword_parameters):
    """
    Tests whether ``StickerPack.banner_url_as`` works as intended.
    
    Parameters
    ----------
    sticker_pack_id : `int`
        Identifier to create sticker pack with.
    
    banner_id : `int`
        banner identifier to create the sticker pack with.
    
    keyword_parameters : `dict<str, object>`
        Additional keyword parameters to pass.
    
    Returns
    -------
    has_banner_url : `bool`
    """
    sticker_pack = StickerPack.precreate(
        sticker_pack_id,
        banner_id = banner_id,
    )
    
    output = sticker_pack.banner_url_as(**keyword_parameters)
    vampytest.assert_instance(output, str, nullable = True)
    return (output is not None)
