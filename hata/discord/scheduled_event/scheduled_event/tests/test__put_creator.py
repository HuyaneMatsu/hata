import vampytest

from ....user import User

from ..fields import put_creator


def _iter_options():
    creator = User.precreate(202303140004, name = 'Orin')
    
    yield creator, True, {'creator': creator.to_data(defaults = True, include_internals = True)}
    yield creator, False, {'creator': creator.to_data(defaults = False, include_internals = True)}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_creator(input_value, defaults):
    """
    Tests whether ``put_creator`` is working as intended.
    
    Parameters
    ----------
    input_value : ``ClientUserBase``
        Value to serialize.
    defaults : `bool`
        Whether fields with their default values should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_creator(input_value, {}, defaults)
