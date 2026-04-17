import vampytest

from ..fields import parse_mentioned_role_ids


def _iter_options():
    role_id_1 = 202305010014
    role_id_2 = 202305010015

    yield {}, None
    yield {'mention_roles': None}, None
    yield {'mention_roles': []}, None
    yield {'mention_roles': [str(role_id_1), str(role_id_2)]}, (role_id_1, role_id_2)
    yield {'mention_roles': [str(role_id_2), str(role_id_1)]}, (role_id_1, role_id_2)


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_mentioned_role_ids(input_data):
    """
    Tests whether ``parse_mentioned_role_ids`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `None | tuple<int>`
    """
    output = parse_mentioned_role_ids(input_data)
    vampytest.assert_instance(output, tuple, nullable = True)
    
    if (output is not None):
        for element in output:
            vampytest.assert_instance(element, int)
    
    return output
