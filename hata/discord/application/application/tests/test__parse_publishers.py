import vampytest

from ...application_entity import ApplicationEntity

from ..fields import parse_publishers


def test__parse_publishers():
    """
    Tests whether ``parse_publishers`` works as intended.
    """
    application_entity = ApplicationEntity.precreate(202211270000)
    
    for input_data, expected_output in (
        ({}, None),
        ({'publishers': None}, None),
        ({'publishers': []}, None),
        (
            {'publishers': [application_entity.to_data(defaults = True, include_internals = True)]},
            (application_entity, )
        )
    ):
        output = parse_publishers(input_data)
        
        vampytest.assert_eq(output, expected_output)
