import vampytest

from ..fields import parse_author_ids


def _iter_options():
    author_id_0 = 202601030006
    author_id_1 = 202601030007
    
    yield (
        {},
        None,
    )
    
    yield (
        {
            'author_id': None,
        },
        None,
    )
    
    yield (
        {
            'author_id': [],
        },
        None,
    )
    
    yield (
        {
            'author_id': [
                str(author_id_0),
                str(author_id_1),
            ],
        },
        (
            author_id_0,
            author_id_1,
        ),
    )
    
    yield (
        {
            'author_id': [
                str(author_id_1),
                str(author_id_0),
            ],
        },
        (
            author_id_0,
            author_id_1,
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_author_ids(input_data):
    """
    Tests whether ``parse_author_ids`` works as intended.
    
    Parameters
    ----------
    data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `None | tuple<int>`
    """
    output = parse_author_ids(input_data)
    vampytest.assert_instance(output, tuple, nullable = True)
    
    if (output is not None):
        for element in output:
            vampytest.assert_instance(element, int)
    
    return output
