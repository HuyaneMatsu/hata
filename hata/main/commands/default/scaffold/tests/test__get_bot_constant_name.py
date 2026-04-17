import vampytest

from ..naming import get_bot_constant_name


def test__get_bot_constant_name():
    """
    Tests whether ``get_bot_constant_name`` works as intended.
    """
    for input_value, expected_output in (
        ('koishi_bot_69', 'KOISHI_BOT_69'),
        ('koishi_bot69', 'KOISHI_BOT_69'),
        ('KoishiBot69', 'KOISHI_BOT_69'),
        ('KOISHI_BOT_69', 'KOISHI_BOT_69'),
        ('koishiBot69', 'KOISHI_BOT_69'),
    ):
        output = get_bot_constant_name(input_value)
        vampytest.assert_instance(output, str)
        vampytest.assert_eq(output, expected_output)
