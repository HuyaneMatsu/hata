import warnings as module_warnings

import vampytest

from ...client import Client


def test__EventHandlerManager__clear():
    """
    Issue: `DeprecationWarning` in `EventHandlerManager.clear`.
    
    Could happen when clearing a deprecated event. These cases should be checked.
    """
    client = Client('token_20220718')
    
    try:
        with module_warnings.catch_warnings(record = True) as warnings:
            module_warnings.simplefilter('always')
            
            client.events.clear()
            
            vampytest.assert_eq(len(warnings), 0)
    finally:
        client._delete()
        client = None
