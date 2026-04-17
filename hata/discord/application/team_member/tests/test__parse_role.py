import vampytest

from ..fields import parse_role
from ..preinstanced import TeamMemberRole


def _iter_options():
    yield {}, TeamMemberRole.none
    yield {'role': TeamMemberRole.admin.value}, TeamMemberRole.admin


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_role(input_data):
    """
    Tests whether ``parse_role`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Input data.
    
    Returns
    -------
    output : ``TeamMemberRole``
    """
    output = parse_role(input_data)
    vampytest.assert_instance(output, TeamMemberRole)
    return output
