import vampytest

from ..fields import put_author_ids


def _iter_options():
    author_id_0 = 202601030008
    author_id_1 = 202601030009
    
    yield (
        None,
        False,
        {},
    )
    
    yield (
        None,
        True,
        {
            'author_id': [],
        },
    )
    
    yield (
        (
            author_id_0,
            author_id_1,
        ),
        False,
        {
            'author_id': [
                str(author_id_0),
                str(author_id_1),
            ],
        },
    )
    
    yield (
        (
            author_id_0,
            author_id_1,
        ),
        True,
        {
            'author_id': [
                str(author_id_0),
                str(author_id_1),
            ],
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_author_ids(input_value, defaults):
    """
    Tests whether ``put_author_ids`` is working as intended.
    
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
    return put_author_ids(input_value, {}, defaults)
