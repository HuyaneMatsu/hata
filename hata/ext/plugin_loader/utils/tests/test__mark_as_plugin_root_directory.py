from importlib.machinery import ModuleSpec, SourceFileLoader
from os.path import join

import vampytest

from ..mark_as_plugin_root_directory_ import mark_as_plugin_root_directory


NAME = 'okuu'
PATH = join('/root', NAME)
FILE_PATH = join(PATH, '__init__.py')


LISTED_ENTRIES = [
    '__init__.py',
    'koishi.py',
    'satori',
    'parsee',
    'yuugi.txt',
    'link',
]


DIRECTORIES = {
    join(PATH, 'satori'),
    join(PATH, 'parsee'),
}

FILES = {
    join(PATH, 'koishi.py'),
    join(PATH, 'yuugi.txt'),
    join(PATH, 'satori', '__init__.py'),
}

def list_directory_mock(path):
    vampytest.assert_eq(path, PATH)
    return LISTED_ENTRIES.copy()

    
def is_directory_mock(path):
    return path in DIRECTORIES


def is_file_mock(path):
    return path in FILES


IMPORTED_PLUGINS = set()

EXPECTED_IMPORTED_PLUGINS = {
    f'{NAME}.koishi',
    f'{NAME}.satori',
}


def import_plugin_mock(path):
    IMPORTED_PLUGINS.add(path)


class DummyFrame:
    f_globals = {
        '__spec__': ModuleSpec(NAME, SourceFileLoader('setup', FILE_PATH), origin = FILE_PATH),
    }


def get_last_module_frame_mock():
    return DummyFrame


def test__mark_as_plugin_root_directory():
    """
    tests whether ``mark_as_plugin_root_directory`` works as intended.
    """
    try:
        mocked = vampytest.mock_globals(
            mark_as_plugin_root_directory,
            list_directory = list_directory_mock,
            is_directory = is_directory_mock,
            is_file = is_file_mock,
            import_plugin = import_plugin_mock,
            get_last_module_frame = get_last_module_frame_mock,
        )
        
        output = mocked()
        vampytest.assert_instance(output, int)
        vampytest.assert_eq(output, len(EXPECTED_IMPORTED_PLUGINS))
        
        vampytest.assert_eq(IMPORTED_PLUGINS, EXPECTED_IMPORTED_PLUGINS)
    
    finally:
        IMPORTED_PLUGINS.clear()
