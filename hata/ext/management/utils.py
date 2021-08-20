from ...backend.futures import render_exc_to_list


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
    render_exc_to_list(exception, extend=extracted)
    return ''.join(extracted)
