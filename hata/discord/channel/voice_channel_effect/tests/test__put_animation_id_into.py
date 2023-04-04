import vampytest

from ..fields import put_animation_id_into


def test__put_animation_id_into():
    """
    Tests whether ``put_animation_id_into`` works as intended.
    """
    animation_id = 202304030012
    
    for input_value, defaults, expected_output in (
        (0, False, {'animation_id': None}),
        (0, True, {'animation_id': None}),
        (animation_id, False, {'animation_id': str(animation_id)}),
    ):
        data = put_animation_id_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
