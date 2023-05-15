import vampytest

from ..naming import get_bot_display_name


def test__get_bot_display_name():
    """
    Tests whether ``get_bot_display_name`` works as intended.
    """
    for input_value, expected_output in (
        ('koishi_bot_69', 'Koishi Bot 69'),
        ('koishi_bot69', 'Koishi Bot 69'),
        ('KoishiBot69', 'Koishi Bot 69'),
        ('KOISHI_BOT_69', 'Koishi Bot 69'),
        ('koishiBot69', 'Koishi Bot 69'),
    ):
        output = get_bot_display_name(input_value)
        vampytest.assert_instance(output, str)
        vampytest.assert_eq(output, expected_output)
