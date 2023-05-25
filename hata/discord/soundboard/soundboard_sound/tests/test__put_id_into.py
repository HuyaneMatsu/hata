import vampytest

from ..fields import put_id_into


def test__put_id_into():
    """
    Tests whether ``put_id_into`` works as intended.
    """
    sound_id = 202305240004
    
    for input_value, defaults, expected_output in (
        (0, False, {'sound_id': None}),
        (0, True, {'sound_id': None}),
        (sound_id, False, {'sound_id': str(sound_id)}),
    ):
        data = put_id_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
