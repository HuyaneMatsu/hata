import vampytest


from ..attachments import _build_partial_attachment_data


def _iter_options():
    yield 1, None, {'id': str(1)}
    yield 2, 'mister', {'id': str(2), 'description': 'mister'}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_partial_attachment_data(attachment_id, description):
    """
    Tests whether ``_build_partial_attachment_data`` works as intended.
    
    Parameters
    ----------
    attachment_id : `int`
        The attachment's identifier.
    description : `None | str`
        Description for the attachment.
    
    Returns
    -------
    data : `dict<str, object>
    """
    return _build_partial_attachment_data(attachment_id, description)
