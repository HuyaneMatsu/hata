import vampytest

from ..shared_fields import put_description


def _iter_options():
    yield (
        '',
        False,
        {
            'description': '',
        },
    )
    
    yield (
        '',
        True,
        {
            'description': '',
        },
    )
    
    yield (
        'a',
        False,
        {
            'description': 'a',
        },
    )
    
    yield (
        'a',
        True,
        {
            'description': 'a',
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_description(input_description, defaults):
    """
    Tests whether ``put_description`` works as intended.
    
    Parameters
    ----------
    input_description : `str`
        The description to serialise.
    
    defaults : `bool`
        Whether descriptions with their default description should be included in the output as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_description(input_description, {}, defaults)
