import vampytest

from ...place_holder import PlaceHolder

from ..preinstanced_meta import _set_slot_place_holders


class TestType():
    __slots__ = ('name', 'value')


def _iter_options():
    yield (
        {
            'hey': 'mister',
            '__slots__': (),
        },
        None,
        (),
        'koishi',
        '',
        {
            'hey': 'mister',
            '__slots__': (),
            'name': PlaceHolder('koishi'),
            'value': PlaceHolder(''),
        }
    )
    
    yield (
        {
            'hey': 'mister',
            '__slots__': ('name', 'value'),
        },
        None,
        ('name', 'value'),
        'koishi',
        '',
        {
            'hey': 'mister',
            '__slots__': ('name', 'value'),
        }
    )
    
    yield (
        {
            'hey': 'mister',
            '__slots__': (),
        },
        TestType,
        (),
        'koishi',
        '',
        {
            'hey': 'mister',
            '__slots__': (),
        }
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__set_slot_place_holders(type_attributes, type_parent, slots, name_default, value_default):
    """
    Tests whether ``_set_slot_place_holders`` works as intended.
    
    Parameters
    ----------
    type_attributes : `dict<str, object>`
        The type attributes of the created type.
    
    type_parent : `None | type`
        Parent type.
    
    slots : `tuple<str>`
        The defined slots of the type.
    
    name_default : `str`
        The default name to use.
    
    value_default : `int | str`
        The default value to use.
    
    Returns
    -------
    type_attributes : `dict<str, object>`
    
    Raises
    ------
    RuntimeError
    TypeError
    """
    type_attributes = type_attributes.copy()
    _set_slot_place_holders(type_attributes, type_parent, slots, name_default, value_default)
    return type_attributes
