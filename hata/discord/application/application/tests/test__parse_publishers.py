import vampytest

from ...application_entity import ApplicationEntity

from ..fields import parse_publishers


def _iter_options():
    application_entity_0 = ApplicationEntity.precreate(202404140000)
    application_entity_1 = ApplicationEntity.precreate(202404140001)
    
    yield {}, None
    yield {'publishers': None}, None
    yield {'publishers': []}, None
    yield (
        {
            'publishers': [
                application_entity_0.to_data(defaults = True, include_internals = True),
            ],
        },
        (application_entity_0, ),
    )
    yield (
        {
            'publishers': [
                application_entity_0.to_data(defaults = True, include_internals = True),
                application_entity_1.to_data(defaults = True, include_internals = True),
            ],
        },
        (application_entity_0, application_entity_1),
    )
    yield (
        {
            'publishers': [
                application_entity_1.to_data(defaults = True, include_internals = True),
                application_entity_0.to_data(defaults = True, include_internals = True),
            ],
        },
        (application_entity_0, application_entity_1),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_publishers(input_data):
    """
    Tests whether ``parse_publishers`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `none | tuple<ApplicationEntity>`
    """
    return parse_publishers(input_data)
