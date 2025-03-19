from scarletio.utils.analyzer import Parameter


def _create_parameter(name, *, annotation = ..., default = ...):
    """
    Creates a parameter.
    
    Parameters
    ----------
    name : `str`
        The name of teh parameter.
    
    annotation : `object`, Optional (Keyword only)
        Annotation of the parameter.
    
    default : `object`, Optional (Keyword only)
        Default value of the parameter.
    
    Returns
    -------
    parameter : ``Parameter``
    """
    parameter = object.__new__(Parameter)
    parameter.annotation = None if annotation is ... else annotation
    parameter.default = None if default is ... else default
    parameter.has_annotation = (annotation is not ...)
    parameter.has_default = (default is not ...)
    parameter.name = name
    parameter.positionality = 2
    parameter.reserved = False
    return parameter
