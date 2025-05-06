import vampytest

from ..fields import put_speaker_ids


def test__put_speaker_ids():
    """
    Tests whether ``put_speaker_ids`` is working as intended.
    """
    speaker_id = 202303120074
    
    for input_value, defaults, expected_output in (
        (None, False, {}),
        (None, True, {'speaker_ids': []}),
        ((speaker_id, ), False, {'speaker_ids': [str(speaker_id)]}),
    ):
        data = put_speaker_ids(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
