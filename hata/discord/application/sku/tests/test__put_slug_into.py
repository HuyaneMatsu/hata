import vampytest

from ..fields import put_slug_into


def _iter_options():
    yield None, False, {}
    yield None, True, {'slug': None}
    yield 'https://orindance.party/', False, {'slug': 'https://orindance.party/'}
    yield 'https://orindance.party/', True, {'slug': 'https://orindance.party/'}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_slug_into(input_value, defaults):
    """
    Tests whether ``put_slug_into`` is working as intended.
    
    Parameters
    ----------
    input_value : `None | str`
        The value to serialise.
    defaults : `bool`
        Whether values with their default value should be included in the output as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_slug_into(input_value, {}, defaults)
