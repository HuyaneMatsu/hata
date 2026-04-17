import vampytest

from ..precreate_helpers import raise_extra


def test__raise_extra__0():
    """
    Tests whether ``raise_extra`` works as intended.
    
    Case: No extra fields.
    """
    raise_extra(None)


def test__raise_extra__1():
    """
    Tests whether ``raise_extra`` works as intended.
    
    Case: Extra fields.
    """
    with vampytest.assert_raises(TypeError):
        raise_extra({'love': 'neko'})
