import vampytest

from ....component import ComponentType

from ..fields import parse_type


def _iter_options():
    yield (
        {},
        ComponentType.none,
    )
    
    yield (
        {
            'type': ComponentType.row.value,
        },
        ComponentType.row,
    )
    
    yield (
        {
            'component_type': ComponentType.row.value,
        },
        ComponentType.row,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_type(input_data):
    """
    Tests whether ``parse_type`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Input data.
    
    Returns
    -------
    output : ``ComponentType``
    """
    output = parse_type(input_data)
    vampytest.assert_instance(output, ComponentType)
    return output
