import vampytest

from ..converters import put_converter_id


def _iter_options():
    entity_id = 202310220016
    yield 0, None
    yield entity_id, str(entity_id)


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_converter_id(input_value):
    """
    Tests whether ``put_converter_id`` works as intended.
    
    Parameters
    ----------
    input_value : `int`
        Processed value.
    
    Returns
    -------
    output : `None | str`
    """
    return put_converter_id(input_value)
