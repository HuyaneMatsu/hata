import vampytest

from ....user import ClientUserBase, User, ZEROUSER

from ..fields import parse_creator


def _iter_options():
    creator = User.precreate(202303140003, name = 'Orin')
    
    yield {}, ZEROUSER
    yield {'creator': None}, ZEROUSER
    yield {'creator': creator.to_data(include_internals = True)}, creator


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_creator(input_data):
    """
    Tests whether ``parse_creator`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : ``ClientUserBase``
    """
    output = parse_creator(input_data)
    vampytest.assert_instance(output, ClientUserBase)
    return output
