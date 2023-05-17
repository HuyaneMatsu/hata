import warnings as module_warnings

import vampytest

from ...sticker import Sticker, StickerFormat

from ..sticker_counts import StickerCounts


def _assert_is_every_attribute_set(sticker_counts):
    """
    Asserts whether every attributes are set of the given sticker counts.
    
    Parameters
    ----------
    sticker_counts : ``StickerCounts``
        The sticker counts to check out.
    """
    vampytest.assert_instance(sticker_counts, StickerCounts)
    vampytest.assert_instance(sticker_counts.animated, int)
    vampytest.assert_instance(sticker_counts.lottie, int)
    vampytest.assert_instance(sticker_counts.static, int)


def _assert_empty(sticker_counts):
    """
    Asserts whether the given sticker joints are empty.
    
    Parameters
    ----------
    sticker_counts : ``StickerCounts``
        The sticker counts to check out.
    """
    vampytest.assert_eq(sticker_counts.animated, 0)
    vampytest.assert_eq(sticker_counts.lottie, 0)
    vampytest.assert_eq(sticker_counts.static, 0)
    

def test__StickerCounts__new__0():
    """
    Tests whether ``StickerCounts.__new__`` works as intended.
    
    Case: No fields given.
    """
    sticker_counts = StickerCounts()
    _assert_is_every_attribute_set(sticker_counts)
    _assert_empty(sticker_counts)


def test__StickerCounts__new__1():
    """
    Tests whether ``StickerCounts.__new__`` works as intended.
    
    Case: All fields given.
    """
    animated = 1
    lottie = 2
    static = 3
    
    sticker_counts = StickerCounts(
        animated = animated,
        lottie = lottie,
        static = static,
    )
    _assert_is_every_attribute_set(sticker_counts)
    
    vampytest.assert_eq(sticker_counts.animated, animated)
    vampytest.assert_eq(sticker_counts.lottie, lottie)
    vampytest.assert_eq(sticker_counts.static, static)


def test__StickerCounts__from_stickers__0():
    """
    Tests whether ``StickerCounts.from_stickers`` works as intended.
    
    Case: Empty iterable given.
    """
    sticker_counts = StickerCounts.from_stickers([])
    _assert_is_every_attribute_set(sticker_counts)
    _assert_empty(sticker_counts)


def test__StickerCounts__from_stickers__1():
    """
    Tests whether ``StickerCounts.from_stickers`` works as intended.
    
    Case: Stuffed iterable given.
    """
    animated_ids = (202212190032,)
    lottie_ids = (202212190033, 202212190034)
    static_ids = (202212190035, 202212190036, 202212190037)
    
    stickers = [
        *(Sticker.precreate(sticker_id, sticker_format = StickerFormat.apng) for sticker_id in animated_ids),
        *(Sticker.precreate(sticker_id, sticker_format = StickerFormat.lottie) for sticker_id in lottie_ids),
        *(Sticker.precreate(sticker_id, sticker_format = StickerFormat.png) for sticker_id in static_ids),
    ]
    
    sticker_counts = StickerCounts.from_stickers(stickers)
    _assert_is_every_attribute_set(sticker_counts)
    
    vampytest.assert_eq(sticker_counts.animated, len(animated_ids))
    vampytest.assert_eq(sticker_counts.lottie, len(lottie_ids))
    vampytest.assert_eq(sticker_counts.static, len(static_ids))


def test__StickerCounts__normal_total():
    """
    Tests whether ``StickerCounts.normal_total`` works as intended.
    """
    animated = 1
    static = 2
    
    expected_value = animated + static
    
    sticker_counts = StickerCounts(
        animated = animated,
        static = static,
    )
    vampytest.assert_eq(sticker_counts.normal_total, expected_value)


def test__StickerCounts__total():
    """
    Tests whether ``StickerCounts.total`` works as intended.
    """
    animated = 1
    lottie = 2
    static = 4
    
    expected_value = animated + lottie + static
    
    sticker_counts = StickerCounts(
        animated = animated,
        lottie = lottie,
        static = static,
    )
    vampytest.assert_eq(sticker_counts.total, expected_value)


def test__StickerCounts__bool():
    """
    Tests whether ``StickerCounts.__bool__`` works as intended.
    """
    for keyword_parameters, expected_output in (
        ({}, False),
        ({'animated': 1}, True),
        ({'lottie': 1}, True),
        ({'static': 1}, True),
    ):
        sticker_counts = StickerCounts(**keyword_parameters)
        vampytest.assert_eq(bool(sticker_counts), expected_output)


def test__StickerCounts__repr():
    """
    Tests whether ``StickerCounts.__repr__`` works as intended.
    """
    animated = 1
    lottie = 2
    static = 3
    
    sticker_counts = StickerCounts(
        animated = animated,
        lottie = lottie,
        static = static,
    )
    
    vampytest.assert_instance(repr(sticker_counts), str)


def test__StickerCounts__eq():
    """
    Tests whether ``StickerCounts.__eq__`` works as intended.
    """
    animated = 1
    lottie = 2
    static = 3
    
    keyword_parameters = {
        'animated': animated,
        'lottie': lottie,
        'static': static,
    }
    
    sticker_counts = StickerCounts(**keyword_parameters)
    
    vampytest.assert_eq(sticker_counts, sticker_counts)
    vampytest.assert_ne(sticker_counts, object())
    
    for field_name, field_value in (
        ('animated', 4),
        ('lottie', 5),
        ('static', 6),

    ):
        test_sticker_counts = StickerCounts(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(sticker_counts, test_sticker_counts)


def test__StickerCounts__hash():
    """
    Tests whether ``StickerCounts.__hash__`` works as intended.
    """
    animated = 1
    lottie = 2
    static = 3
    
    sticker_counts = StickerCounts(
        animated = animated,
        lottie = lottie,
        static = static,
    )
    
    vampytest.assert_instance(hash(sticker_counts), int)


def test__StickerCounts__iter():
    """
    Tests whether ``StickerCounts.__iter__`` works as intended. This field is deprecated.
    """
    animated = 1
    lottie = 2
    static = 3
    
    sticker_counts = StickerCounts(
        animated = animated,
        lottie = lottie,
        static = static,
    )
    
    with module_warnings.catch_warnings(record = True) as warnings:
        module_warnings.simplefilter('always')
        
        unpacked = [*sticker_counts]
        
        vampytest.assert_eq(len(warnings), 1)
    
    vampytest.assert_eq(unpacked, [static, animated, lottie])
