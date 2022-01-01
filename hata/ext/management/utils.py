from os import makedirs as make_directories
from os.path import join as join_paths

from scarletio.utils.trace import render_exception_into


def render_exception(exception):
    """
    Renders the given exception.
    
    Parameters
    ----------
    exception : ``BaseException``
        The exception to render it's traceback.
    
    Returns
    -------
    traceback : `str`
    """
    extracted = []
    render_exception_into(exception, extend=extracted)
    return ''.join(extracted)


def create_file_structure(directory, structure):
    """
    Creates the listed files based on the given structure.
    
    Parameters
    ----------
    directory : `str`
        Directory to execute the file creation.
    structure : `tuple` of `tuple` (`tuple` of (`str`, `None`), (`str`, `None`))
        File structure to create.
    """
    for paths, file_content in structure:
        paths_length = len(paths)
        
        file_name = paths[paths_length - 1]
        
        if paths_length == 1:
            paths = None
        else:
            paths = paths[:paths_length - 1]
        
        if (paths is None):
            folder_path = directory
        else:
            folder_path = join_paths(directory, *paths)
            make_directories(folder_path, exist_ok=True)
        
        if (file_name is not None):
            file_path = join_paths(folder_path, file_name)
            
            file = open(file_path, 'w')
            
            if (file_content is not None):
                file.write(file_content)
            
            file.close()
