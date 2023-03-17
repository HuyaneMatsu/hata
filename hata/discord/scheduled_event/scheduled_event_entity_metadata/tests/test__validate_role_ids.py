import vampytest

from ....user import User

from ..fields import validate_speaker_ids


def test__validate_speaker_ids__0():
    """
    Tests whether `validate_speaker_ids` works as intended.
    
    Case: passing.
    """
    speaker_id_1 = 202303120075
    speaker_id_2 = 202303120076
    
    for input_value, expected_output in (
        (None, None),
        ([], None),
        ([speaker_id_2, speaker_id_1], (speaker_id_1, speaker_id_2)),
        ([User.precreate(speaker_id_1)], (speaker_id_1, )),
    ):
        output = validate_speaker_ids(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_speaker_ids__1():
    """
    Tests whether `validate_speaker_ids` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
        [12.6],
    ):
        with vampytest.assert_raises(TypeError):
            validate_speaker_ids(input_value)
