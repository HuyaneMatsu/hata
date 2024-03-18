import vampytest

from ..builder_base import _collect_default_conversions

from .helpers import _create_default_conversion, TestType


def _iter_options():
    conversion_0 = _create_default_conversion({
        'name': 'satori'
    })
    conversion_1 = _create_default_conversion({
        'name': 'satori',
    })
    
    yield (
        (),
        {},
        [],
    )
    
    yield (
        (),
        {'__conversions_default__': [conversion_0]},
        [conversion_0],
    )

    yield (
        (
            TestType({'CONVERSIONS_DEFAULT': [conversion_0]}),
        ),
        {},
        [conversion_0],
    )
    yield (
        (
            TestType({'CONVERSIONS_DEFAULT': [conversion_0]}),
        ),
        {'__conversions_default__': [conversion_1]},
        [conversion_0, conversion_1],
    )

    yield (
        (
            TestType({'CONVERSIONS_DEFAULT': [conversion_0]}),
        ),
        {'__conversions_default__': [conversion_0]},
        [conversion_0],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__collect_default_conversions(builder_types, type_attributes):
    """
    Tests whether ``_collect_default_conversions`` works as intended.
    
    Parameters
    ----------
    builder_types : `list<type>`
        Inherited builder types to collect from.
    type_attributes : `dict<str, object>`
        The type attributes of the type to be created.
    
    Returns
    -------
    output : `list<Conversion>`
    """
    return _collect_default_conversions(builder_types, type_attributes)
