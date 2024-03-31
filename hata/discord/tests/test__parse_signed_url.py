from datetime import datetime as DateTime

import vampytest

from ..utils import parse_signed_url

from .test__SignedUrlParseResult import _assert_fields_set


def _iter_options():
    yield (
        (
            'https://cdn.discordapp.com/attachments/1012345678900020080/1234567891233211234/my_image.png'
            '?ex=65d903de&is=65c68ede&hm=2481f30dd67f503f54d020ae3b5533b9987fae4e55f2b4e3926e08a3fa3ee24f'
        ),
        (
            'https://cdn.discordapp.com/attachments/1012345678900020080/1234567891233211234/my_image.png',
            DateTime(2024,  2,  9, 20, 45, 18),
            DateTime(2024,  2, 23, 20, 45, 18),
            b'$\x81\xf3\r\xd6\x7fP?T\xd0 \xae;U3\xb9\x98\x7f\xaeNU\xf2\xb4\xe3\x92n\x08\xa3\xfa>\xe2O',
        )
    )
    
    yield (
        (
            'https://cdn.discordapp.com/attachments/1012345678900020080/1234567891233211234/my_image.png'
        ),
        (
            'https://cdn.discordapp.com/attachments/1012345678900020080/1234567891233211234/my_image.png',
            None,
            None,
            None,
        )
    )
    
    yield (
        (
            'https://cdn.discordapp.com/attachments/1012345678900020080/1234567891233211234/my_image.png'
            '?ex=65dp03de&is=65c68ede&hm=2481f30dd67f503f54d020ae3b5533b9987fae4e55f2b4e3926e08a3fa3ee24f'
        ),
        (
            'https://cdn.discordapp.com/attachments/1012345678900020080/1234567891233211234/my_image.png',
            DateTime(2024,  2,  9, 20, 45, 18),
            None,
            b'$\x81\xf3\r\xd6\x7fP?T\xd0 \xae;U3\xb9\x98\x7f\xaeNU\xf2\xb4\xe3\x92n\x08\xa3\xfa>\xe2O',
        )
    )
    yield (
        (
            'https://cdn.discordapp.com/attachments/1012345678900020080/1234567891233211234/my_image.png'
            '?ex=65d903de&is=65cp8ede&hm=2481f30dd67f503f54d020ae3b5533b9987fae4e55f2b4e3926e08a3fa3ee24f'
        ),
        (
            'https://cdn.discordapp.com/attachments/1012345678900020080/1234567891233211234/my_image.png',
            None,
            DateTime(2024,  2, 23, 20, 45, 18),
            b'$\x81\xf3\r\xd6\x7fP?T\xd0 \xae;U3\xb9\x98\x7f\xaeNU\xf2\xb4\xe3\x92n\x08\xa3\xfa>\xe2O',
        )
    )
    yield (
        (
            'https://cdn.discordapp.com/attachments/1012345678900020080/1234567891233211234/my_image.png'
            '?ex=65d903de&is=65c68ede&hm=2481f30dd67f503f54d020ae3b5533b9987fae4p55f2b4e3926e08a3fa3ee24f'
        ),
        (
            'https://cdn.discordapp.com/attachments/1012345678900020080/1234567891233211234/my_image.png',
            DateTime(2024,  2,  9, 20, 45, 18),
            DateTime(2024,  2, 23, 20, 45, 18),
            None,
        )
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_signed_url(input_value):
    """
    Tests whether ``parse_signed_url`` works as intended.
    
    Parameters
    ----------
    input_value : `str`
        Value to test with.
    
    Returns
    -------
    output : `(str, None | DateTime, None | DateTime, None | bytes)`
    """
    result = parse_signed_url(input_value)
    _assert_fields_set(result)
    return result.url, result.signed_at, result.expires_at, result.signature
