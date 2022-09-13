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
        Slowmode applied for created threads in the channel.
    
    Returns
    -------
    topic : `None`, `str`
    
    Raises
    ------
    TypeError
        - If `topic` is not `None`, `str`.
    ValueError
        - If `topic` is out of the expected range.
    """
    if (topic is not None):
        topic = preconvert_str(topic, 'topic', 0, 1024)
        if not topic:
            topic = None
    
    return topic
