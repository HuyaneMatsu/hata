import vampytest

from ..fields import put_mentioned_user_ids


def _iter_options():
    user_id_0 = 202601030022
    user_id_1 = 202601030023
    
    yield (
        None,
        False,
        {},
    )
    
    yield (
        None,
        True,
        {
            'mentions': [],
        },
    )
    
    yield (
        (
            user_id_0,
            user_id_1,
        ),
        False,
        {
            'mentions': [
                str(user_id_0),
                str(user_id_1),
            ],
        },
    )
    
    yield (
        (
            user_id_0,
            user_id_1,
        ),
        True,
        {
            'mentions': [
                str(user_id_0),
                str(user_id_1),
            ],
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_mentioned_user_ids(input_value, defaults):
    """
    Tests whether ``put_mentioned_user_ids`` is working as intended.
    
    Parameters
    ----------
    input_value : `None | tuple<int>`
        The value to serialise.
    
    defaults : `bool`
        Whether fields as their defaults should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_mentioned_user_ids(input_value, {}, defaults)
