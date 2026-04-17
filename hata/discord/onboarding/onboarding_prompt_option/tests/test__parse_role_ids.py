import vampytest

from ..fields import parse_role_ids


def _iter_options():
    role_id_0 = 202303030000
    role_id_1 = 202303030001
    
    yield (
        {},
        None,
    )
    
    yield (
        {
            'role_ids': None,
        },
        None,
    )
    
    yield (
        {
            'role_ids': [],
        },
        None,
    )
    
    yield (
        {
            'role_ids': [
                str(role_id_0),
                str(role_id_1),
            ],
        },
        (
            role_id_0,
            role_id_1,
        )
    )
    
    yield (
        {
            'role_ids': [
                str(role_id_1),
                str(role_id_0),
            ],
        },
        (
            role_id_0,
            role_id_1,
        )
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_role_ids(input_data):
    """
    Tests whether ``parse_role_ids`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `None | tuple<int>`
    """
    output = parse_role_ids(input_data)
    vampytest.assert_instance(output, tuple, nullable = True)
    return output
