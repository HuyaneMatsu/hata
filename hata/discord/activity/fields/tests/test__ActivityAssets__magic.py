import vampytest

from .. import ActivityAssets


def test__ActivityAssets__repr():
    """
    Tests whether ``ActivityAssets.__repr__`` works as intended.
    """
    field = ActivityAssets(
        image_large = 'plain',
        image_small = 'asia',
        text_large = 'senya',
        text_small = 'vocal',
    )
    
    vampytest.assert_instance(repr(field), str)


def test__ActivityAssets__eq():
    """
    Tests whether ``ActivityAssets.__repr__`` works as intended.
    """
    fields = {
        'image_large': 'plain',
        'image_small': 'asia',
        'text_large': 'senya',
        'text_small': 'vocal',
    }
    
    field_original = ActivityAssets(**fields)
    
    vampytest.assert_eq(field_original, field_original)
    
    for field_name in (
        'image_large',
        'image_small',
        'text_large',
        'text_small',
    ):
        field_altered = ActivityAssets(**{**fields, field_name: None})
        vampytest.assert_ne(field_original, field_altered)


def test__ActivityAssets__hash():
    """
    Tests whether ``ActivityAssets.__hash__`` works as intended.
    """
    field = ActivityAssets(
        image_large = 'plain',
        image_small = 'asia',
        text_large = 'senya',
        text_small = 'vocal',
    )
    
    vampytest.assert_instance(hash(field), int)


def test__ActivityAssets__bool():
    """
    Tests whether ``ActivityAssets.__bool__`` works as intended.
    """
    field = ActivityAssets()
    
    field_bool = bool(field)
    vampytest.assert_instance(field_bool, bool)
    vampytest.assert_false(field_bool)
    
    
    for field_name in (
        'image_large',
        'image_small',
        'text_large',
        'text_small',
    ):
        field = ActivityAssets(**{field_name: 'trance'})
        
        field_bool = bool(field)
        vampytest.assert_instance(field_bool, bool)
        vampytest.assert_true(field_bool)
