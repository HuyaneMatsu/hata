import vampytest

from .....env import API_VERSION

from ..fields import put_flags__serialisation
from ..flags import ApplicationFlag


def _iter_options():
    yield (
        ApplicationFlag(0),
        False,
        {},
    )
    
    if API_VERSION < 10:
        yield (
            ApplicationFlag(0),
            True,
            {
                'flags': 0,
            },
        )
        
        yield (
            ApplicationFlag(1),
            False,
            {
                'flags': 1,
            },
        )
        
        yield (
            ApplicationFlag(1),
            True,
            {
                'flags': 1,
            },
        )
    
    else:
        yield (
            ApplicationFlag(0),
            True,
            {
                'flags_new': '0',
            },
        )
        
        yield (
            ApplicationFlag(1),
            False,
            {
                'flags_new': '1',
            },
        )
        
        yield (
            ApplicationFlag(1),
            True,
            {
                'flags_new': '1',
            },
        )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_flags__serialisation(input_value, defaults):
    """
    Tests whether ``put_flags__serialisation`` is working as intended.
    
    Parameters
    ----------
    input_value : ``ApplicationFlag``
        The value to serialise.
    
    defaults : `bool`
        Whether fields of their default value should be included in the output.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    return put_flags__serialisation(input_value, {}, defaults)
