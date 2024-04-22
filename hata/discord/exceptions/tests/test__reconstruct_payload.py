import vampytest
from scarletio import to_json
from scarletio.web_common import FormData

from ..payload_renderer import reconstruct_payload


def _iter_options():
    yield None, None
    yield to_json({'hey': 'mister'}), 'payload = {\n    "hey": "mister",\n}'
    yield 'hey)mister', 'payload = "hey)mister"'
    yield b'hey mister', 'payload = Binary<length = 10>'
    
    form_data_0 = FormData()
    yield form_data_0, 'payload = FormData()'
    
    form_data_1 = FormData()
    form_data_1.add_field('hey', b'mister')
    form_data_1.add_json('pudding', 'eater')
    
    yield form_data_1, 'payload = FormData({\n    0: "hey": Binary<length = 6>,\n    1: "pudding": "eater",\n})'


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__reconstruct_payload(input_value):
    """
    Tests whether ``reconstruct_payload`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to test with.
    Returns
    -------
    output : `None | str`
    """
    output = reconstruct_payload(input_value)
    vampytest.assert_instance(output, str, nullable = True)
    return output
