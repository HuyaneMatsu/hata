__all__ = ()

class Filter:
    """
    Represents filters applied to a solar client.
    
    Adding a filter can have adverse effects on performance. Filters force the lava player to decode all audio to PCM,
    even if the input was already in the Opus format that Discord uses. This means decoding and encoding audio that
    would normally require very little processing. This is often the case with YouTube videos.
    
    
    """

