import vampytest

from ..fields import put_attachment_id


def _iter_options():
    attachment_id = 202509200002
    
    yield (
        0,
        True,
        {
            'attachment_id': None,
        },
    )
    
    yield (
        0,
        True,
        {
            'attachment_id': None,
        },
    )
    
    yield (
        attachment_id,
        False,
        {
            'attachment_id': str(attachment_id),
        },
    )
    
    yield (
        attachment_id,
        True,
        {
            'attachment_id': str(attachment_id),
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_attachment_id(input_value, defaults):
    """
    Tests whether ``put_attachment_id`` works as intended.
    
    Parameters
    ----------
    input_value : `int`
        The value to serialise.
    
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_attachment_id(input_value, {}, defaults)
