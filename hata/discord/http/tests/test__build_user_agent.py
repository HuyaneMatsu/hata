from sys import implementation

import vampytest

from ..headers import build_user_agent


def test__build_user_agent__with_appendix():
    """
    Tests whether ``build_user_agent`` works as intended.
    
    Case: with appendix.
    """
    base = 'koishi'
    appendix = 'satori'
    
    mocked = vampytest.mock_globals(
        build_user_agent, LIBRARY_AGENT_APPENDIX = appendix,
    )
    
    output = mocked(base)
    
    vampytest.assert_instance(output, str)
    vampytest.assert_eq(output, f'{base!s} {appendix!s}')


def test__build_user_agent__final():
    """
    Tests whether ``build_user_agent`` works as intended.
    
    Case: final release.
    """
    base = 'koishi'
    implementation_name = 'orin'
    version_major = 3
    version_minor = 6
    version_release_level = 'final'
    
    mocked = vampytest.mock_globals(
        build_user_agent,
        LIBRARY_AGENT_APPENDIX = None,
        implementation = type(implementation)(
            name = implementation_name,
            version = (version_major, version_minor, 0, version_release_level, 123456),
        ),
    )
    
    output = mocked(base)
    
    vampytest.assert_instance(output, str)
    vampytest.assert_eq(output, f'{base!s} Python ({implementation_name!s} {version_major!s}.{version_minor!s})')


def test__build_user_agent__not_final():
    """
    Tests whether ``build_user_agent`` works as intended.
    
    Case: not final release.
    """
    base = 'koishi'
    implementation_name = 'orin'
    version_major = 3
    version_minor = 6
    version_release_level = 'alpha'
    
    mocked = vampytest.mock_globals(
        build_user_agent,
        LIBRARY_AGENT_APPENDIX = None,
        implementation = type(implementation)(
            name = implementation_name,
            version = (version_major, version_minor, 0, version_release_level, 123456),
        ),
    )
    
    output = mocked(base)
    
    vampytest.assert_instance(output, str)
    vampytest.assert_eq(
        output,
        f'{base!s} Python ({implementation_name!s} {version_major!s}.{version_minor!s} {version_release_level!s})',
    )
