import vampytest

from ...application_entity import ApplicationEntity

from ..fields import parse_developers


def test__parse_developers():
    """
    Tests whether ``parse_developers`` works as intended.
    """
    application_entity = ApplicationEntity.precreate(202211270000)
    
    for input_data, expected_output in (
        ({}, None),
        ({'developers': None}, None),
        ({'developers': []}, None),
        (
            {'developers': [application_entity.to_data(defaults = True, include_internals = True)]},
            (application_entity, )
        )
    ):
        output = parse_developers(input_data)
        
        vampytest.assert_eq(output, expected_output)
