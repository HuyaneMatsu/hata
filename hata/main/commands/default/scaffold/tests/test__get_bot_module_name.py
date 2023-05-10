import vampytest

from ..naming import get_bot_module_name


def test__get_bot_module_name():
    """
    Tests whether ``get_bot_module_name`` works as intended.
    """
    for input_value, expected_output in (
        ('koishi_bot_69', 'koishi_bot_69'),
        ('koishi_bot69', 'koishi_bot_69'),
        ('KoishiBot69', 'koishi_bot_69'),
        ('KOISHI_BOT_69', 'koishi_bot_69'),
        ('koishiBot69', 'koishi_bot_69'),
    ):
        output = get_bot_module_name(input_value)
        vampytest.assert_instance(output, str)
        vampytest.assert_eq(output, expected_output)
