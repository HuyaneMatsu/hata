import vampytest

from ..profiling import build_package_not_installed


def test__build_package_not_installed():
    """
    Test whether ``build_package_not_installed`` works as intended.
    """
    def get_short_executable():
        return 'python3'
    
    name = 'satori'
    
    mocked = vampytest.mock_globals(
        build_package_not_installed,
        get_short_executable = get_short_executable,
    )
    
    output = mocked(name)
    
    vampytest.assert_instance(output, str)
    vampytest.assert_eq(
        output,
        (
            'Required package: \'satori\' is not installed, cannot show profiling result.\n'
            '\n'
            'To install it do:\n'
            '\n'
            '```\n'
            '$ python3 -m pip install satori\n'
            '```\n'
        ),
    )
