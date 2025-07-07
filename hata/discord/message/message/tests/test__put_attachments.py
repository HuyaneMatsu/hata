import vampytest

from ...attachment import Attachment

from ..fields import put_attachments


def _iter_options():
    attachment_id_0 = 202304290007
    attachment_name_0 = 'Primrose'
    
    attachment_id_1 = 202304290008
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
        False,
        {},
    )
    
    yield (
        None,
        True,
        False,
        {
            'attachments': [],
        },
    )
    
    yield (
        (attachment_0, attachment_1),
        False,
        False,
        {
            'attachments': [
                attachment_0.to_data(defaults = False, include_internals = False),
                attachment_1.to_data(defaults = False, include_internals = False),
            ],
        },
    )
    
    yield (
        (attachment_0, attachment_1),
        True,
        False,
        {
            'attachments': [
                attachment_0.to_data(defaults = True, include_internals = False),
                attachment_1.to_data(defaults = True, include_internals = False),
            ],
        },
    )
    
    yield (
        (attachment_0, attachment_1),
        True,
        True,
        {
            'attachments': [
                attachment_0.to_data(defaults = True, include_internals = True),
                attachment_1.to_data(defaults = True, include_internals = True),
            ],
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_attachments(input_value, defaults, include_internals):
    """
    Tests whether ``put_attachments`` works as intended.
    
    Parameters
    ----------
    input_value : ``None | tuple<Attachment>``
        Value to serialize.
    defaults : `bool`
        Whether values as their defaults should be included as well.
    include_internals : `bool`
        Whether internals should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_attachments(input_value, {}, defaults, include_internals = include_internals)
