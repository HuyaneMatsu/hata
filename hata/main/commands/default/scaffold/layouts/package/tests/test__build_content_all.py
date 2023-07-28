import vampytest

from ..readme_rendering import build_readme_content
from ..structure import build_bots_init_file_content, build_constants_file_content, build_dot_env_file_content


@vampytest.call_with(build_readme_content, ('satori', ['red', 'heart'],))
@vampytest.call_with(build_dot_env_file_content, (['red', 'heart'],))
@vampytest.call_with(build_bots_init_file_content, (['red', 'heart'],))
@vampytest.call_with(build_constants_file_content, (['red', 'heart'],))
def test__build_content_all(function, parameters):
    """
    Tests whether ``build_readme_content`` works as intended.
    
    Parameters
    ----------
    function : `(*object) -> str`
        The content creator function to test.
    parameters : `tuple<object>`
        Parameters to pass to `function`.
    """
    output = function(*parameters)
    vampytest.assert_instance(output, str)
