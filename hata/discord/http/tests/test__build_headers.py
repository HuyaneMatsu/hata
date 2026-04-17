import vampytest
from scarletio import IgnoreCaseMultiValueDictionary
from scarletio.web_common.headers import AUTHORIZATION, USER_AGENT

from ..headers import DEBUG_OPTIONS, LIBRARY_USER_AGENT, build_headers


def _iter_options():
    yield (
        True,
        'koishi',
        None,
        IgnoreCaseMultiValueDictionary([
            (USER_AGENT, LIBRARY_USER_AGENT),
            (AUTHORIZATION, f'Bot koishi'),
        ])
    )

    yield (
        False,
        'koishi',
        None,
        IgnoreCaseMultiValueDictionary([
            (USER_AGENT, LIBRARY_USER_AGENT),
            (AUTHORIZATION, 'koishi'),
        ])
    )

    yield (
        True,
        'koishi',
        {'canary', 'alpha'},
        IgnoreCaseMultiValueDictionary([
            (USER_AGENT, LIBRARY_USER_AGENT),
            (AUTHORIZATION, f'Bot koishi'),
            (DEBUG_OPTIONS, 'alpha'),
            (DEBUG_OPTIONS, 'canary'),
        ])
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_headers(bot, token, debug_options):
    """
    Tests whether ``build_headers`` works as intended.
    
    Parameters
    ----------
    bot : `bool`
        Whether the respective client is a bot.
    token : `str`
        The client's token.
    debug_options: `None | set<str>`
        Http debug options.
    
    Returns
    -------
    output : ``IgnoreCaseMultiValueDictionary``
    """
    output = build_headers(bot, token, debug_options)
    vampytest.assert_instance(output, IgnoreCaseMultiValueDictionary)
    return output
