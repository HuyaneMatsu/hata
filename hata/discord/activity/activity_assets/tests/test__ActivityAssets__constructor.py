import vampytest

from ..assets import ActivityAssets


def _assert_fields_set(field):
    """
    Checks whether every attribute is set of the given activity assets field.
    
    Parameters
    ----------
    field : ``ActivityAssets``
        The field to check.
    """
    vampytest.assert_instance(field, ActivityAssets)
    vampytest.assert_instance(field.image_large, str, nullable = True)
    vampytest.assert_instance(field.image_small, str, nullable = True)
    vampytest.assert_instance(field.text_large, str, nullable = True)
    vampytest.assert_instance(field.text_small, str, nullable = True)


def test__ActivityAssets__new__0():
    """
    Tests whether ``ActivityAssets.__new__`` works as intended.
    
    Case: No fields given.
    """
    field = ActivityAssets()
    _assert_fields_set(field)


def test__ActivityAssets__new__1():
    """
    Tests whether ``ActivityAssets.__new__`` works as intended.
    
    Case: Fields given.
    """
    image_large = 'plain'
    image_small = 'asia'
    text_large = 'senya'
    text_small = 'vocal'
    
    field = ActivityAssets(
        image_large = image_large,
        image_small = image_small,
        text_large = text_large,
        text_small = text_small,
    )
    _assert_fields_set(field)
    
    vampytest.assert_eq(field.image_large, image_large)
    vampytest.assert_eq(field.image_small, image_small)
    vampytest.assert_eq(field.text_large, text_large)
    vampytest.assert_eq(field.text_small, text_small)
