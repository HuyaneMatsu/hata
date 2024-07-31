from ....http import DiscordApiClient


class TestDiscordApiClient(DiscordApiClient):
    __slots__ = ('__dict__',)
    
    async def discord_request(self, handler, method, url, data = None, params = None, headers = None, reason = None):
        raise RuntimeError('Real request during testing.')


IMAGE_DATA = (
    b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x19\x00\x00\x00\x19\x08\x06\x00\x00\x00\xc4\xe9\x85c\x00\x00\x00'
    b'\x19IDATx\x9c\xed\xc1\x01\r\x00\x00\x00\xc2\xa0\xf7Om\x0f\x07\x14\x00\x007\x06\t\xdd\x00\x01\x03\x97c\xd5\x00'
    b'\x00\x00\x00IEND\xaeB`\x82'
)
