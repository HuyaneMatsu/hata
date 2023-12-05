import vampytest

from ..fields import put_interaction_version_into
from ..preinstanced import ApplicationInteractionVersion


def _iter_options():
    yield (
        ApplicationInteractionVersion.selective,
        False,
        {'interactions_version': ApplicationInteractionVersion.selective.value},
    )
    yield (
        ApplicationInteractionVersion.selective,
        True,
        {'interactions_version': ApplicationInteractionVersion.selective.value},
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_interaction_version_into(input_value, defaults):
    """
    Tests whether ``put_interaction_version_into`` is working as intended.
    
    Parameters
    ----------
    input_value : ``ApplicationInteractionVersion``
        Input value.
    defaults : `bool`
        Whether fields with their default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    return put_interaction_version_into(input_value, {}, defaults)
