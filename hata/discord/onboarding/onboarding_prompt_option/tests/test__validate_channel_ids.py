import vampytest

from ....channel import Channel

from ..fields import validate_channel_ids


def test__validate_channel_ids__0():
    """
    Tests whether `validate_channel_ids` works as intended.
    
    Case: passing.
    """
    channel_id_1 = 202303030003
    channel_id_2 = 202303030004
    
    for input_value, expected_output in (
        (None, None),
        ([], None),
        ([channel_id_2, channel_id_1], (channel_id_1, channel_id_2)),
        ([Channel.precreate(channel_id_1)], (channel_id_1, )),
    ):
        output = validate_channel_ids(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_channel_ids__1():
    """
    Tests whether `validate_channel_ids` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
        [12.6],
    ):
        with vampytest.assert_raises(TypeError):
            validate_channel_ids(input_value)
