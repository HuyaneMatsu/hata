import vampytest

from ..preinstanced_meta import _get_and_validate_slots


def _iter_options__passing():
    yield (
        {},
        (
            {
                '__slots__': (),
            },
            (),
        ),
    )
    
    yield (
        {
            '__slots__': ('name', 'value'),
        },
        (
            {
                '__slots__': ('name', 'value'),
            },
            ('name', 'value'),
        ),
    )


def _iter_options__type_error():
    yield (
        {
            '__slots__': ['name', 'value'],
        },
    )
    
    yield (
        {
            '__slots__': ['name', 12.6],
        },
    )



@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__get_and_validate_slots(type_attributes):
    """
    Tests whether ``_get_and_validate_slots`` works as intended.
    
    Parameters
    ----------
    type_attributes : `dict<str, object>`
        The type attributes of the created type.
    
    Returns
    -------
    type_attributes : `dict<str, object>`
    output : `tuple<str>`
    
    Raises
    ------
    RuntimeError
    TypeError
    """
    type_attributes = type_attributes.copy()
    output = _get_and_validate_slots(type_attributes)
    vampytest.assert_instance(output, tuple)
    return type_attributes, output
