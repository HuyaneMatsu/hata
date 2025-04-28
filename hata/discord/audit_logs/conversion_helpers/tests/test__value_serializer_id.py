import vampytest

from ..converters import value_serializer_id


def _iter_options():
    entity_id = 202310220016
    yield 0, None
    yield entity_id, str(entity_id)


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__value_serializer_id(input_value):
    """
    Tests whether ``value_serializer_id`` works as intended.
    
    Parameters
    ----------
    input_value : `int`
        Processed value.
    
    Returns
    -------
    output : `None | str`
    """
    output = value_serializer_id(input_value)
    vampytest.assert_instance(output, str, nullable = True)
    return output

