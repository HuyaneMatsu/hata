__all__ = ()


def parse_topic(data):
    """
    Parses out the `topic` field from the given data.
    
    Parameters
    ----------
    data : `dict` of (`str`, `Any`) items
        Channel data.
    
    Returns
    -------
    topic : `None`, `str`
    """
    topic = data.get('topic', None)
    if (topic is not None) and (not topic):
        topic = None
    
    return topic
