__all__ = ()

from ...preconverters import preconvert_str

from ..constants import TOPIC_LENGTH_MAX, TOPIC_LENGTH_MIN


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


def validate_topic(topic):
    """
    Validates the given `topic` field.
    
    Parameters
    ----------
    topic : `None`, `str`
        The channel's topic.
    
    Returns
    -------
    topic : `None`, `str`
    
    Raises
    ------
    TypeError
        - If `topic` is not `None`, `str`.
    ValueError
        - If `topic`'s length is out of the expected range.
    """
    if (topic is not None):
        topic = preconvert_str(topic, 'topic', TOPIC_LENGTH_MIN, TOPIC_LENGTH_MAX)
        if not topic:
            topic = None
    
    return topic


def put_topic_into(topic, data, defaults):
    """
    Puts the `topic`'s data into the given `data` json serializable object.
    
    Parameters
    ----------
    topic : `None`, `str`
        The channel's topic.
    data : `dict` of (`str`, `Any`) items
        Json serializable dictionary.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict` of (`str`, `Any`) items
    """
    if topic is None:
        topic = ''
    
    data['topic'] = topic
    
    return data
