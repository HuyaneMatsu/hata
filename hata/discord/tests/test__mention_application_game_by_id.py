import vampytest

from ..utils import mention_application_game_by_id


def test__mention_application_game_by_id():
    """
    Tests whether ``mention_application_game_by_id`` works as intended.
    """
    application_id = 202607040000
    
    output = mention_application_game_by_id(application_id)
    vampytest.assert_instance(output, str)
    vampytest.assert_eq(output, f'<@${application_id}>')
