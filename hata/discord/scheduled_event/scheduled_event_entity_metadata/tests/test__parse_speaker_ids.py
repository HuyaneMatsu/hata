import vampytest

from ..fields import parse_speaker_ids


def test__parse_speaker_ids():
    """
    Tests whether ``parse_speaker_ids`` works as intended.
    """
    speaker_id_1 = 202303120072
    speaker_id_2 = 202303120073
    
    for input_data, expected_output in (
        ({}, None),
        ({'speaker_ids': None}, None),
        ({'speaker_ids': []}, None),
        ({'speaker_ids': [str(speaker_id_1), str(speaker_id_2)]}, (speaker_id_1, speaker_id_2)),
        ({'speaker_ids': [str(speaker_id_2), str(speaker_id_1)]}, (speaker_id_1, speaker_id_2)),
    ):
        output = parse_speaker_ids(input_data)
        vampytest.assert_eq(output, expected_output)
