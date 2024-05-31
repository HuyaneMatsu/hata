import vampytest

from ...attachment import Attachment

from ..fields import put_attachments_into


def _iter_options():
    attachment_id_0 = 202405240003
    attachment_name_0 = 'Primrose'
    
    attachment_id_1 = 202405240004
    attachment_name_1 = 'Flower'
    
    attachment_0 = Attachment.precreate(
        attachment_id_0,
        name = attachment_name_0,
    )
    
    attachment_1 = Attachment.precreate(
        attachment_id_1,
        name = attachment_name_1,
    )
    
    yield (
        None,
        False,
        {}
    )
    
    yield (
        None,
        True,
        {
            'message': {
                'attachments': [],
            },
        },
    )
    
    yield (
        (attachment_0, attachment_1),
        False,
        {
            'message': {
                'attachments': [
                    attachment_0.to_data(defaults = False, include_internals = True),
                    attachment_1.to_data(defaults = False, include_internals = True),
                ],
            },
        },
    )
    
    yield (
        (attachment_0, attachment_1),
        True,
        {
            'message': {
                'attachments': [
                    attachment_0.to_data(defaults = True, include_internals = True),
                    attachment_1.to_data(defaults = True, include_internals = True),
                ],
            },
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_attachments_into(input_value, defaults):
    """
    Tests whether ``put_attachments_into`` works as intended.
    
    Parameters
    ----------
    input_value : `None | tuple<Attachment>`
        Value to serialize.
    defaults : `bool`
        Whether values as their defaults should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_attachments_into(input_value, {}, defaults)
