import vampytest

from ..fields import parse_pack_id


def test__parse_pack_id():
    """
    Tests whether ``parse_pack_id`` works as intended.
    """
    pack_id = 202301040005
    
    for input_data, expected_output in (
        ({}, 0),
        ({'pack_id': None}, 0),
        ({'pack_id': str(pack_id)}, pack_id),
    ):
        output = parse_pack_id(input_data)
        vampytest.assert_eq(output, expected_output)
