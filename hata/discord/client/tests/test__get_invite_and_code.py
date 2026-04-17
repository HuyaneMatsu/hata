import vampytest

from ...invite import Invite

from ..request_helpers import get_invite_and_code


def _iter_options__passing():
    invite_code = 'koishi'
    
    yield (
        invite_code,
        [],
        (None, invite_code),
    )
    
    invite_code = 'satori'
    invite = Invite.precreate(invite_code) 
    
    yield (
        invite,
        [invite],
        (invite, invite_code),
    )
    
    invite_code = 'okuu'
    invite = Invite.precreate(invite_code) 
    
    yield (
        invite_code,
        [invite],
        (invite, invite_code),
    )


def _iter_options__type_error():
    yield None, []
    yield 12.6, []


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__get_invite_and_code(input_value, extra):
    """
    Tests whether ``get_invite_and_code`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Input value to test with.
    
    extra : `list<object>`
        Extra objects to keep in cache.
    
    Returns
    -------
    output : ``(None | Invite, str)``
    
    Raises
    ------
    TypeError
    """
    output = get_invite_and_code(input_value)
    
    vampytest.assert_instance(output, tuple)
    vampytest.assert_eq(len(output), 2)
    invite, invite_code = output
    vampytest.assert_instance(invite, Invite, nullable = True)
    vampytest.assert_instance(invite_code, str)
    
    return output
