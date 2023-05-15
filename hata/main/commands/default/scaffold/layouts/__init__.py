__all__ = ()

from importlib import import_module


LAYOUT_DESCRIPTIONS = {
    'package': (
        'Package layout\'s main benefit is that allows easier installation and management of your application.\n'
        'With it you can use package managers like pip or conda simplifying deployment.\n'
        'This also makes it easier to distribute your application between multiple developers.\n'
        '\n'
        'An other benefit is that it helps avoiding naming conflicts (in other words name pollution) when installing\n'
        'since it provides a namespace for your code.\n'
        '\n'
        'Structure:\n'
        '```\n'
        'root\n'
        '├─ .gitignore\n'
        '├─ README.md\n'
        '├─ pyproject.toml\n'
        '└─ { project }\n'
        '    ├─ .env\n'
        '    ├─ __init__.py\n'
        '    ├─ __main__.py\n'
        '    ├─ cli.py\n'
        '    ├─ bots\n'
        '    │   ├─ __init__.py\n'
        '    │   ├─ { bot_names[n] }.py\n'
        '    │   └─ ...\n'
        '    └─ plugins\n'
        '        └─ __init__.py\n'
        '```\n'
    )
}

DEFAULT_LAYOUT = 'package'


MISSING_LAYOUT_APPENDIX = f'Are you sure the name is correct? Perhaps the layout\'s definition is missing?'


def get_project_structure_builder(layout):
    """
    Gets the project structure builder for the given layout.
    
    Parameters
    ----------
    layout : `str`
        The layout to get the builder for.
    
    Returns
    -------
    project_structure_builder : `(str, str, list<str>) -> None`
    
    Raises
    ------
    RuntimeError
        - If layout is missing or if it does not have `create_project_structure` defined.
    """
    try:
        module = import_module(f'{__spec__.parent}.{layout}')
    except ImportError as err:
        raise RuntimeError(
            f'Layout `{layout}` could not be found.\n{MISSING_LAYOUT_APPENDIX}'
        ) from err
    
    try:
        project_structure_builder = module.create_project_structure
    except AttributeError as err:
        raise RuntimeError(
            f'Layout `{layout}` does not have project structure builder defined.\n{MISSING_LAYOUT_APPENDIX}'
        ) from err
    
    return project_structure_builder
