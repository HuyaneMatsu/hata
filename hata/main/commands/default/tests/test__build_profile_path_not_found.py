import vampytest

from ..profiling import build_profile_path_not_found


def test__build_profile_path_not_found():
    """
    Tests whether ``build_profile_path_not_found`` works as intended.
    """
    def render_main_call_into(into):
        into.append('python3')
        into.append(' ')
        into.append('-m')
        into.append(' ')
        into.append('koishi')
        return into
    
    mocked = vampytest.mock_globals(
        build_profile_path_not_found,
        render_main_call_into = render_main_call_into,
    )
    
    name = 'satori'
    
    output = mocked(name)
    
    vampytest.assert_instance(output, str)
    vampytest.assert_eq(
        output,
        (
            'Profile file with name: \'satori\' not found.\n'
            'Try using "$ python3 -m koishi profile list" to list the available profiling results.\n'
        ),
    )
