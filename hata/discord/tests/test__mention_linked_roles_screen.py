import vampytest

from ..utils import mention_linked_roles_screen


def _iter_options():
    yield (
        0,
        '<id:linked-roles>',
    )
    
    role_id = 202511100000
    
    yield (
        role_id,
        f'<id:linked-roles:{role_id!s}>',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__mention_linked_roles_screen(role_id):
    """
    Tests whether ``mention_linked_roles_screen`` works as intended.
    
    Parameters
    ----------
    role_id : `int`
        A specific role to reference.
    
    Returns
    -------
    output : `str`
    """
    output = mention_linked_roles_screen(role_id)
    vampytest.assert_instance(output, str)
    return output
