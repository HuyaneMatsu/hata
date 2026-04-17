import vampytest

from ....permission import Permission

from ..fields import parse_user_permissions


def _iter_options():
    yield (
        {},
        Permission(),
    )
    
    yield (
        {
            'is_nickname_changeable': None,
        },
        Permission(),
    )
    
    yield (
        {
            'is_nickname_changeable': False,
        },
        Permission(),
    )
    
    yield (
        {
            'is_nickname_changeable': True,
        },
        Permission().update_by_keys(
            change_nickname = True,
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_user_permissions(input_data):
    """
    Tests whether ``parse_user_permissions`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : ``Permission``
    """
    output = parse_user_permissions(input_data)
    vampytest.assert_instance(output, Permission)
    return output
