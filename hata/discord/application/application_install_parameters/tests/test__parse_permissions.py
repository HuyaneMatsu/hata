import vampytest

from ....permission import Permission

from ..fields import parse_permissions


def _iter_options():
    yield (
        {},
        Permission(),
    )
    
    yield (
        {
            'permissions': None,
        },
        Permission(),
    )
    
    yield (
        {
            'permissions': '1',
        },
        Permission(1),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_permissions(input_data):
    """
    Tests whether ``parse_permissions`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : ``Permission``
    """
    output = parse_permissions(input_data)
    vampytest.assert_instance(output, Permission)
    return output
