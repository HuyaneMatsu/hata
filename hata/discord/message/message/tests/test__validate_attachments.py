import vampytest

from ...attachment import Attachment

from ..fields import validate_attachments


def _iter_options__passing():
    attachment_id_0 = 202304290009
    attachment_id_1 = 202304290010
    
    attachment_0 = Attachment.precreate(attachment_id_0)
    attachment_1 = Attachment.precreate(attachment_id_1)
    
    yield None, None
    yield [], None
    yield [attachment_0], (attachment_0,)
    yield [attachment_1, attachment_0], (attachment_0, attachment_1)


def _iter_options__type_error():
    yield 12.6
    yield [12.6]


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_attachments(input_value):
    """
    Validates whether ``validate_attachments`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Returns
    -------
    output : `None | tuple<Attachment>`
    
    Raises
    ------
    TypeError
    """
    output = validate_attachments(input_value)
    vampytest.assert_instance(output, tuple, nullable = True)
    return output
