import vampytest

from ..fields import parse_id


def test__parse_id():
    """
    Tests whether ``parse_id`` works as intended.
    """
    sound_id = 202305240003
    
    for input_data, expected_output in (
        ({}, 0),
        ({'sound_id': None}, 0),
        ({'sound_id': str(sound_id)}, sound_id),
    ):
        output = parse_id(input_data)
        vampytest.assert_eq(output, expected_output)
