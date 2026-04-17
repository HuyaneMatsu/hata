__all__ = ('PollVoteDeleteEvent',)

from .add import PollVoteAddEvent


class PollVoteDeleteEvent(PollVoteAddEvent):
    """
    Represents a processed `MESSAGE_POLL_VOTE_REMOVE` dispatch event.
    
    Attributes
    ----------
    answer_id : `int`
        The voted answer's identifier.
    message : ``Message``
        The message from what the vote was removed.
    user_id : `int`
        The user's identifier who removed their vote.
    """
    __slots__ = ()
