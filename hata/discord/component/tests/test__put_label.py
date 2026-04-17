import vampytest

from ..shared_fields import put_label


def _iter_options():
    yield (
        '',
        False,
        {
            'label': '',
        },
    )
    
    yield (
        '',
        True,
        {
            'label': '',
        },
    )
    
    yield (
        'a',
        False,
        {
            'label': 'a',
        },
    )
    
    yield (
        'a',
        True,
        {
            'label': 'a',
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_label(input_label, defaults):
    """
    Tests whether ``put_label`` works as intended.
    
    Parameters
    ----------
    input_label : `str`
        The label to serialise.
    
    defaults : `bool`
        Whether labels with their default label should be included in the output as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_label(input_label, {}, defaults)
