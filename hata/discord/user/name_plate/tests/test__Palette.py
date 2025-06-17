import vampytest

from ....color import Color

from ..preinstanced import Palette


def _assert_fields_set(palette):
    """
    Asserts whether every field are set of the given voice region.
    
    Parameters
    ----------
    palette : ``Palette``
        The instance to test.
    """
    vampytest.assert_instance(palette, Palette)
    vampytest.assert_instance(palette.name, str)
    vampytest.assert_instance(palette.value, Palette.VALUE_TYPE)
    vampytest.assert_instance(palette.color, Color)


@vampytest.call_from(Palette.INSTANCES.values())
def test__Palette__instances(instance):
    """
    Tests whether ``Palette`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``Palette``
        The instance to test.
    """
    _assert_fields_set(instance)
