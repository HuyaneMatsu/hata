import vampytest

from ..readme_rendering import (
    render_readme_section_project_into, render_readme_section_running, render_readme_section_scaffold,
    render_readme_section_structure_bot, render_readme_section_structure_bots,
    render_readme_section_structure_bots_init, render_readme_section_structure_cli,
    render_readme_section_structure_constants, render_readme_section_structure_directory_into,
    render_readme_section_structure_dot_env, render_readme_section_structure_gitignore_into,
    render_readme_section_structure_into, render_readme_section_structure_main, render_readme_section_structure_plugins,
    render_readme_section_structure_plugins_init, render_readme_section_structure_plugins_ping,
    render_readme_section_structure_project, render_readme_section_structure_project_init,
    render_readme_section_structure_pyproject, render_readme_section_structure_readme_into
)


@vampytest.call_with(render_readme_section_project_into, ('satori', ))
@vampytest.call_with(render_readme_section_scaffold, ())
@vampytest.call_with(render_readme_section_structure_into, ('satori', ['red', 'heart']))
@vampytest.call_with(render_readme_section_structure_directory_into, ('satori', ['red', 'heart']))
@vampytest.call_with(render_readme_section_structure_gitignore_into, ())
@vampytest.call_with(render_readme_section_structure_readme_into, ())
@vampytest.call_with(render_readme_section_structure_pyproject, ())
@vampytest.call_with(render_readme_section_structure_project, ('satori', ))
@vampytest.call_with(render_readme_section_structure_dot_env, ('satori', ))
@vampytest.call_with(render_readme_section_structure_project_init, ('satori', ))
@vampytest.call_with(render_readme_section_structure_main, ('satori', ))
@vampytest.call_with(render_readme_section_structure_cli, ('satori', ))
@vampytest.call_with(render_readme_section_structure_bots, ('satori', ))
@vampytest.call_with(render_readme_section_structure_bots_init, ('satori', ['red', 'heart']))
@vampytest.call_with(render_readme_section_structure_bot, ('satori', 'red'))
@vampytest.call_with(render_readme_section_structure_plugins, ('satori', ))
@vampytest.call_with(render_readme_section_structure_plugins_init, ('satori', ))
@vampytest.call_with(render_readme_section_structure_plugins_ping, ('satori',))
@vampytest.call_with(render_readme_section_running, ('satori', ))
@vampytest.call_with(render_readme_section_structure_constants, ('satori',))
def test_renderer(function, parameters):
    """
    Tests whether the given `render_into` function works as intended.
    
    Parameters
    ----------
    function : `(list<str>, *object) -> list<str>`
        Renderer function to call.
    parameters : `tuple<object>`
        The parameters to pass into the function.
    """
    output = function([], *parameters)
    
    vampytest.assert_instance(output, list)
    for value in output:
        vampytest.assert_instance(value, str)
