from datetime import datetime as DateTime

import vampytest

from ..utils import SignedUrlParseResult


def _assert_fields_set(result):
    """
    Asserts whether every fields are set of the given signed url result.
    
    Parameters
    ----------
    result : ``SignedUrlParseResult``
        The result to test.
    """
    vampytest.assert_instance(result, SignedUrlParseResult)
    vampytest.assert_instance(result.expires_at, DateTime, nullable = True)
    vampytest.assert_instance(result.signature, bytes, nullable = True)
    vampytest.assert_instance(result.signed_at, DateTime, nullable = True)
    vampytest.assert_instance(result.url, str)


def test__DateTime__new():
    """
    Tests whether ``DateTime.__new__`` works as intended.
    """
    url = 'https://cdn.discordapp.com/attachments/1012345678900020080/1234567891233211234/my_image.png'
    signed_at  = DateTime(2024,  2,  9, 20, 45, 18)
    expires_at = DateTime(2024,  2, 23, 20, 45, 18)
    signature = b'$\x81\xf3\r\xd6\x7fP?T\xd0 \xae;U3\xb9\x98\x7f\xaeNU\xf2\xb4\xe3\x92n\x08\xa3\xfa>\xe2O'
    
    result = SignedUrlParseResult(url, signed_at, expires_at, signature)
    _assert_fields_set(result)
    
    vampytest.assert_eq(result.url, url)
    vampytest.assert_eq(result.signed_at, signed_at)
    vampytest.assert_eq(result.expires_at, expires_at)
    vampytest.assert_eq(result.signature, signature)


def test__SignedUrlParseResult__repr():
    """
    Tests whether ``SignedUrlParseResult.__repr__`` works as intended.
    """
    url = 'https://cdn.discordapp.com/attachments/1012345678900020080/1234567891233211234/my_image.png'
    signed_at  = DateTime(2024,  2,  9, 20, 45, 18)
    expires_at = DateTime(2024,  2, 23, 20, 45, 18)
    signature = b'$\x81\xf3\r\xd6\x7fP?T\xd0 \xae;U3\xb9\x98\x7f\xaeNU\xf2\xb4\xe3\x92n\x08\xa3\xfa>\xe2O'
    
    result = SignedUrlParseResult(url, signed_at, expires_at, signature)
    
    output = repr(result)
    
    vampytest.assert_instance(output, str)
    vampytest.assert_in(type(result).__name__, output)
    vampytest.assert_in(f'url = {url!r}', output)
    vampytest.assert_in(f'signed_at = {signed_at!r}', output)
    vampytest.assert_in(f'expires_at = {expires_at!r}', output)
    vampytest.assert_in(f'signature = {signature!r}', output)


def _iter_options__eq__same_type():
    yield (
        (
            'https://cdn.discordapp.com/attachments/1012345678900020080/1234567891233211234/my_image.png',
            DateTime(2024,  2,  9, 20, 45, 18),
            DateTime(2024,  2, 23, 20, 45, 18),
            b'$\x81\xf3\r\xd6\x7fP?T\xd0 \xae;U3\xb9\x98\x7f\xaeNU\xf2\xb4\xe3\x92n\x08\xa3\xfa>\xe2O',
        ),
        (
            'https://cdn.discordapp.com/attachments/1012345678900020080/1234567891233211234/my_image.png',
            DateTime(2024,  2,  9, 20, 45, 18),
            DateTime(2024,  2, 23, 20, 45, 18),
            b'$\x81\xf3\r\xd6\x7fP?T\xd0 \xae;U3\xb9\x98\x7f\xaeNU\xf2\xb4\xe3\x92n\x08\xa3\xfa>\xe2O',
        ),
        True,
    )
    
    yield (
        (
            'https://cdn.discordapp.com/attachments/1012345678900020080/1234567891233211234/image.png',
            DateTime(2024,  2,  9, 20, 45, 18),
            DateTime(2024,  2, 23, 20, 45, 18),
            b'$\x81\xf3\r\xd6\x7fP?T\xd0 \xae;U3\xb9\x98\x7f\xaeNU\xf2\xb4\xe3\x92n\x08\xa3\xfa>\xe2O',
        ),
        (
            'https://cdn.discordapp.com/attachments/1012345678900020080/1234567891233211234/my_image.png',
            DateTime(2024,  2,  9, 20, 45, 18),
            DateTime(2024,  2, 23, 20, 45, 18),
            b'$\x81\xf3\r\xd6\x7fP?T\xd0 \xae;U3\xb9\x98\x7f\xaeNU\xf2\xb4\xe3\x92n\x08\xa3\xfa>\xe2O',
        ),
        False,
    )
    
    yield (
        (
            'https://cdn.discordapp.com/attachments/1012345678900020080/1234567891233211234/my_image.png',
            None,
            DateTime(2024,  2, 23, 20, 45, 18),
            b'$\x81\xf3\r\xd6\x7fP?T\xd0 \xae;U3\xb9\x98\x7f\xaeNU\xf2\xb4\xe3\x92n\x08\xa3\xfa>\xe2O',
        ),
        (
            'https://cdn.discordapp.com/attachments/1012345678900020080/1234567891233211234/my_image.png',
            DateTime(2024,  2,  9, 20, 45, 18),
            DateTime(2024,  2, 23, 20, 45, 18),
            b'$\x81\xf3\r\xd6\x7fP?T\xd0 \xae;U3\xb9\x98\x7f\xaeNU\xf2\xb4\xe3\x92n\x08\xa3\xfa>\xe2O',
        ),
        False,
    )
    
    yield (
        (
            'https://cdn.discordapp.com/attachments/1012345678900020080/1234567891233211234/my_image.png',
            DateTime(2024,  2,  9, 20, 45, 18),
            None,
            b'$\x81\xf3\r\xd6\x7fP?T\xd0 \xae;U3\xb9\x98\x7f\xaeNU\xf2\xb4\xe3\x92n\x08\xa3\xfa>\xe2O',
        ),
        (
            'https://cdn.discordapp.com/attachments/1012345678900020080/1234567891233211234/my_image.png',
            DateTime(2024,  2,  9, 20, 45, 18),
            DateTime(2024,  2, 23, 20, 45, 18),
            b'$\x81\xf3\r\xd6\x7fP?T\xd0 \xae;U3\xb9\x98\x7f\xaeNU\xf2\xb4\xe3\x92n\x08\xa3\xfa>\xe2O',
        ),
        False,
    )
    
    yield (
        (
            'https://cdn.discordapp.com/attachments/1012345678900020080/1234567891233211234/my_image.png',
            DateTime(2024,  2,  9, 20, 45, 18),
            DateTime(2024,  2, 23, 20, 45, 18),
            None,
        ),
        (
            'https://cdn.discordapp.com/attachments/1012345678900020080/1234567891233211234/my_image.png',
            DateTime(2024,  2,  9, 20, 45, 18),
            DateTime(2024,  2, 23, 20, 45, 18),
            b'$\x81\xf3\r\xd6\x7fP?T\xd0 \xae;U3\xb9\x98\x7f\xaeNU\xf2\xb4\xe3\x92n\x08\xa3\xfa>\xe2O',
        ),
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq__same_type()).returning_last())
def test__SignedUrlParseResult__eq__same_type(parameters_0, parameters_1):
    """
    Tests whether ``SignedUrlParseResult.__eq__`` works as intended.
    
    Case: same type.
    
    Parameters
    ----------
    parameters_0 : `tuple<object>`
        Parameters to create result from.
    parameters_0 : `tuple<object>`
        Parameters to create result from.
    
    Returns
    -------
    output : `bool`
    """
    result_0 = SignedUrlParseResult(*parameters_0)
    result_1 = SignedUrlParseResult(*parameters_1)
    
    output = result_0 == result_1
    vampytest.assert_instance(output, bool)
    return output


def _iter_options__eq__different_type():
    yield None, False
    yield object(), False


@vampytest._(vampytest.call_from(_iter_options__eq__different_type()).returning_last())
def test__SignedUrlParseResult__eq__different_type(other):
    """
    Tests whether ``SignedUrlParseResult.__eq__`` works as intended.
    
    Case: different type.
    
    Parameters
    ----------
    other : `object`
        Other object to compare the result to.
    
    Returns
    -------
    output : `bool`
    """
    url = 'https://cdn.discordapp.com/attachments/1012345678900020080/1234567891233211234/my_image.png'
    signed_at  = DateTime(2024,  2,  9, 20, 45, 18)
    expires_at = DateTime(2024,  2, 23, 20, 45, 18)
    signature = b'$\x81\xf3\r\xd6\x7fP?T\xd0 \xae;U3\xb9\x98\x7f\xaeNU\xf2\xb4\xe3\x92n\x08\xa3\xfa>\xe2O'
    
    result = SignedUrlParseResult(url, signed_at, expires_at, signature)
    
    output = result == other
    vampytest.assert_instance(output, bool)
    return output


def test__SignedUrlParseResult__hash():
    """
    Tests whether ``SignedUrlParseResult.__hash__`` works as intended.
    """
    url = 'https://cdn.discordapp.com/attachments/1012345678900020080/1234567891233211234/my_image.png'
    signed_at  = DateTime(2024,  2,  9, 20, 45, 18)
    expires_at = DateTime(2024,  2, 23, 20, 45, 18)
    signature = b'$\x81\xf3\r\xd6\x7fP?T\xd0 \xae;U3\xb9\x98\x7f\xaeNU\xf2\xb4\xe3\x92n\x08\xa3\xfa>\xe2O'
    
    result = SignedUrlParseResult(url, signed_at, expires_at, signature)
    
    output = hash(result)
    vampytest.assert_instance(output, int)
