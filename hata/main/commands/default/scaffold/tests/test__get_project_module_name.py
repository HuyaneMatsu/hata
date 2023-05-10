from os.path import join as join_paths

import vampytest

from ..naming import get_project_module_name


def test__get_project_module_name():
    """
    Tests whether ``get_project_module_name`` works as intended.
    """
    for input_value, expected_output in (
        ('koishi_bot_69', 'koishi_bot_69'),
        ('koishi_bot69', 'koishi_bot_69'),
        ('KoishiBot69', 'koishi_bot_69'),
        ('KOISHI_BOT_69', 'koishi_bot_69'),
        ('koishiBot69', 'koishi_bot_69'),
        (join_paths('koishi', 'koishi_bot_69'), 'koishi_bot_69'),
        (join_paths('koishi', 'koishi_bot69'), 'koishi_bot_69'),
        (join_paths('koishi', 'KoishiBot69'), 'koishi_bot_69'),
        (join_paths('koishi', 'KOISHI_BOT_69'), 'koishi_bot_69'),
        (join_paths('koishi', 'koishiBot69'), 'koishi_bot_69'),
    ):
        output = get_project_module_name(input_value)
        vampytest.assert_instance(output, str)
        vampytest.assert_eq(output, expected_output)
