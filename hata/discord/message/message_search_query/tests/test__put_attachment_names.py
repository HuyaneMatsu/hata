import vampytest

from ..fields import put_attachment_names


def _iter_options():
    yield (
        None,
        False,
        {},
    )
    
    yield (
        None,
        True,
        {
            'attachment_filename': [],
        },
    )
    
    yield (
        (
            'fry',
            'shrimp',
        ),
        False,
        {
            'attachment_filename': [
                'fry',
                'shrimp',
            ],
        },
    )
    
    yield (
        (
            'fry',
            'shrimp',
        ),
        True,
        {
            'attachment_filename': [
                'fry',
                'shrimp',
            ],
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_attachment_names(input_value, defaults):
    """
    Tests whether ``put_attachment_names`` is working as intended.
    
    Parameters
    ----------
    input_value : `None | tuple<str>`
        The value to serialise.
    
    defaults : `bool`
        Whether fields as their defaults should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_attachment_names(input_value, {}, defaults)
