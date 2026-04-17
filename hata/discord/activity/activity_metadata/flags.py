__all__ = ('ActivityFlag', )

from ...bases import FlagBase, FlagDescriptor as F


class ActivityFlag(FlagBase):
    """
    The flags of an activity provided by Discord. These flags supposed to describe what the activity's payload
    includes.
    
    The activity flags are the following:
    
    +-------------------------------+-------------------+
    | Respective name               | Bitwise position  |
    +===============================+===================+
    | instance                      | 0                 |
    +-------------------------------+-------------------+
    | join                          | 1                 |
    +-------------------------------+-------------------+
    | spectate                      | 2                 |
    +-------------------------------+-------------------+
    | join_request                  | 3                 |
    +-------------------------------+-------------------+
    | sync                          | 4                 |
    +-------------------------------+-------------------+
    | play                          | 5                 |
    +-------------------------------+-------------------+
    | party_privacy_friends         | 6                 |
    +-------------------------------+-------------------+
    | party_privacy_voice_channel   | 7                 |
    +-------------------------------+-------------------+
    | embedded                      | 8                 |
    +-------------------------------+-------------------+
    | contextless                   | 9                 |
    +-------------------------------+-------------------+
    """
    instance = F(0)
    join = F(1)
    spectate = F(2)
    join_request = F(3)
    sync = F(4)
    play = F(5)
    party_privacy_friends = F(6)
    party_privacy_voice_channel = F(7)
    embedded = F(8)
    contextless = F(9)
