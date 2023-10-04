import vampytest

from ....guild import Guild
from ....role import Role
from ....user import User

from ..fields import validate_owner
from ..preinstanced import EntitlementOwnerType


def _iter_options__passing():
    owner_id = 202310030003
    
    yield None, (EntitlementOwnerType.none, 0)
    yield Guild.precreate(owner_id), (EntitlementOwnerType.guild, owner_id)
    yield User.precreate(owner_id), (EntitlementOwnerType.user, owner_id)
    yield (EntitlementOwnerType.user, owner_id), (EntitlementOwnerType.user, owner_id)
    yield (EntitlementOwnerType.user.value, str(owner_id)), (EntitlementOwnerType.user, owner_id)


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
def test__validate_owner__passing(input_value):
    """
    Tests whether `validate_owner` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Input value to validate.
    
    Returns
    -------
    output : `(EntitlementOwnerType, int)`
    """
    return validate_owner(input_value)


@vampytest.raising(TypeError)
@vampytest.call_with(12.6)
@vampytest.call_with(Role.precreate(202310030004))
@vampytest.call_with(202310030005)
def test__validate_owner__type_error(input_value):
    """
    Tests whether `validate_owner` works as intended.
    
    Case: `TypeError`.
    
    Parameters
    ----------
    input_value : `object`
        Input value to validate.
    
    Raises
    ------
    TypeError
        The occurred exception.
    """
    validate_owner(input_value)


@vampytest.raising(ValueError)
@vampytest.call_with((1, 2, 3))
@vampytest.call_with((1, ))
def test__validate_owner__value_error(input_value):
    """
    Tests whether `validate_owner` works as intended.
    
    Case: `ValueError`.
    
    Parameters
    ----------
    input_value : `object`
        Input value to validate.
    
    Raises
    ------
    ValueError
        The occurred exception.
    """
    validate_owner(input_value)
