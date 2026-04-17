import vampytest

from ....user import User

from ..fields import validate_speaker_ids


def _iter_options__passing():
    speaker_id_0 = 202303120075
    speaker_id_1 = 202303120076
    
    yield None, None
    yield [], None
    yield [speaker_id_0, speaker_id_1], (speaker_id_0, speaker_id_1)
    yield [speaker_id_1, speaker_id_0], (speaker_id_0, speaker_id_1)
    yield [User.precreate(speaker_id_0), User.precreate(speaker_id_1)], (speaker_id_0, speaker_id_1)


def _iter_options__type_error():
    yield 12.6
    yield [12.6]


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_speaker_ids(input_value):
    """
    Tests whether `validate_speaker_ids` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Returns
    -------
    output : `None | tuple<int>`
    
    Raises
    ------
    TypeError
    """
    output = validate_speaker_ids(input_value)
    vampytest.assert_instance(output, tuple, nullable = True)
    return output
